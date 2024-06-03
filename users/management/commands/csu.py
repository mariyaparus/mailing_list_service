from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(
            email='cat-she@mail.ru',
            first_name='Mariya',
            last_name='Parus',
            is_staff=True,
            is_superuser=True
        )

        user.set_password('12345qwerty')
        user.save()