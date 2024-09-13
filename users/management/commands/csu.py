import os

from django.core.management import BaseCommand
from dotenv import load_dotenv

from config.settings import BASE_DIR
from users.models import User

dot_env = os.path.join(BASE_DIR, ".env")
load_dotenv(dotenv_path=dot_env)


class Command(BaseCommand):
    """Команда создания суперпользователя"""

    def handle(self, *args, **options):
        user = User.objects.create(
            email=os.getenv("CSU_EMAIL"),
            first_name=os.getenv("CSU_FIRST_NAME"),
            last_name=os.getenv("CSU_LAST_NAME"),
            phone_number=os.getenv("CSU_PHONE_NUMBER"),
            is_superuser=True,
            is_staff=True,
        )

        user.set_password(os.getenv("CSU_PASSWORD"))
        user.save()
