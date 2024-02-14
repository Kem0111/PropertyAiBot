import os
import django
import csv
from django.core.exceptions import ValidationError


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


def create_super_user():
    from django.contrib.auth.models import User
    from dotenv import load_dotenv

    load_dotenv()

    USERNAME = os.getenv("DJANGO_SUPERUSER_USERNAME", "admin")
    EMAIL = os.getenv("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
    PASSWORD = os.getenv("DJANGO_SUPERUSER_PASSWORD", "password")

    if not User.objects.filter(username=USERNAME).exists():
        User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)


create_super_user()
