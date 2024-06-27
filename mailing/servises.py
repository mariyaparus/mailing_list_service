import datetime
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import send_mail

from mailing.models import Logs
import logging

logger = logging.getLogger(__name__)


def send_email_to_clients(mailing_settings):
    clients = mailing_settings.client.all()
    clients_list = [client.email for client in clients]

    server_response = None
    status = Logs.STATUS_ERROR

    try:
        letter = send_mail(
            subject=mailing_settings.message.theme,
            message=mailing_settings.message.message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=clients_list,
        )

        if letter:
            status = Logs.STATUS_OK
            server_response = "Email sent successfully"

    except SMTPException as e:
        server_response = str(e)
        logger.error(f"SMTPException occurred: {e}")
    else:
        logger.info("Email sent successfully")

    if server_response:
        logger.info(f"Server response: {server_response}")

    Logs.objects.create(
        status=status,
        mailing=mailing_settings,
        server_response=server_response
    )
