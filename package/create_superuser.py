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


def import_properties_from_csv(csv_file_path):
    from bot.models import Property
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            try:
                property, created = Property.objects.update_or_create(
                    id=row['ID'],  # Используйте ID из CSV для сохранения того же ID в модели
                    defaults={
                        'id': row['ID'],
                        'type': row['Тип'],
                        'details': row['Описание'],
                        'location': row['Локация'],
                        'price': row['Цена'],
                        'currency': row['Валюта'],
                        'is_passed': False  # Установите ваше значение по умолчанию
                    }
                )
                if created:
                    print(f'Created property: {property}')
                else:
                    print(f'Updated property: {property}')
            except ValidationError as e:
                print(f"Error creating/updating property: {e}")
            except Exception as e:
                print(f"Unexpected error: {e}")


create_super_user()
import_properties_from_csv('properties.csv')
