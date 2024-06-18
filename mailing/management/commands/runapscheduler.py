# runapscheduler.py
import logging
from django.utils import timezone

from django.conf import settings

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django_apscheduler import util

from mailing.models import Mailing, Logs
from mailing.servises import send_email_to_clients

logger = logging.getLogger(__name__)


def my_job():
    now = timezone.now()

    for mailing_setting in Mailing.objects.filter(status=Mailing.STATUS_STARTED):
        last_attempt = Logs.objects.filter(settings=mailing_setting).order_by('-attempt_date').first()

        if last_attempt:
            last_attempt_date = last_attempt.attempt_date
            time_difference = now - last_attempt_date

            if mailing_setting.period == Mailing.PERIOD_DAILY and time_difference.days >= 1:
                next_send_time = last_attempt_date + timezone.timedelta(days=1, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    send_email_to_clients(mailing_setting)
                    logger.info(f"Email sent to clients for Mailing {mailing_setting.id}")

            elif mailing_setting.period == Mailing.PERIOD_WEEKLY and time_difference.days >= 7:
                next_send_time = last_attempt_date + timezone.timedelta(weeks=1, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    send_email_to_clients(mailing_setting)
                    logger.info(f"Email sent to clients for Mailing {mailing_setting.id}")

            elif mailing_setting.period == Mailing.PERIOD_MONTHLY and time_difference.days >= 30:
                next_send_time = last_attempt_date + timezone.timedelta(days=30, hours=mailing_setting.time.hour,
                                                                        minutes=mailing_setting.time.minute)
                if now >= next_send_time:
                    send_email_to_clients(mailing_setting)
                    logger.info(f"Email sent to clients for Mailing {mailing_setting.id}")

        else:
            send_time = timezone.datetime(now.year, now.month, now.day, mailing_setting.time.hour,
                                          mailing_setting.time.minute, tzinfo=timezone.get_current_timezone())
            if now >= send_time:
                send_email_to_clients(mailing_setting)
                logger.info(f"Email sent to clients for Mailing {mailing_setting.id}")


# The `close_old_connections` decorator ensures that database connections, that have become
# unusable or are obsolete, are closed before and after your job has run. You should use it
# to wrap any jobs that you schedule that access the Django database in any way.
@util.close_old_connections
def delete_old_job_executions(max_age=604_800):
    """
    This job deletes APScheduler job execution entries older than `max_age` from the database.
    It helps to prevent the database from filling up with old historical records that are no
    longer useful.

    :param max_age: The maximum length of time to retain historical job execution records.
                    Defaults to 7 days.
    """
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")

        scheduler.add_job(
            my_job,
            trigger=CronTrigger(second="*/60"),  # Every 60 seconds
            id="my_job",  # The `id` assigned to each job MUST be unique
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'my_job'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")
