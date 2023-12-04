# Generated by Django 4.2.7 on 2023-11-26 15:32

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Покупателя',
                'verbose_name_plural': 'Покупатели',
            },
        ),
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_unread', models.PositiveIntegerField(default=0, verbose_name='Количество непрочитанных сообщений')),
                ('last_message_created', models.DateTimeField(blank=True, default=None, null=True, verbose_name='Дата создания последнего сообщения')),
            ],
            options={
                'verbose_name': 'Чат',
                'verbose_name_plural': 'Чаты',
                'ordering': ['-count_unread'],
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('type', models.CharField(verbose_name='Тип обьекта')),
                ('details', models.TextField(verbose_name='Описание обьекта')),
                ('location', models.CharField(max_length=100, verbose_name='Местоположение')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Цена')),
                ('currency', models.CharField(max_length=9, unique=True, verbose_name='Валюта')),
                ('is_passed', models.BooleanField(default=False, verbose_name='Сдан?')),
            ],
            options={
                'verbose_name': 'Недвижимость',
                'verbose_name_plural': 'Недвижимость',
                'ordering': ['created'],
            },
        ),
        migrations.CreateModel(
            name='TgUser',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('id', models.BigIntegerField(primary_key=True, serialize=False, verbose_name='ID пользователя в Telegram')),
                ('username', models.CharField(blank=True, default=None, max_length=255, null=True, verbose_name='Имя пользователя')),
                ('full_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Полное имя')),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True, verbose_name='Номер')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Электронная почта')),
                ('url', models.CharField(max_length=255, unique=True, verbose_name='Ссылка на пользователя')),
                ('has_previous_inquiries', models.BooleanField(blank=True, default=False, null=True, verbose_name='Обращался или нет')),
            ],
            options={
                'verbose_name': 'Телеграм пользователя',
                'verbose_name_plural': 'Телеграм пользователи',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
            ],
            options={
                'verbose_name': 'Администратора',
                'verbose_name_plural': 'Администраторы сайта',
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserThread',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('threade', models.CharField(max_length=150, verbose_name='Идентификатор треда')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bot.tguser', verbose_name='Пользователь')),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bot.tguser', verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Собственника',
                'verbose_name_plural': 'Собственники',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('message_id', models.PositiveIntegerField(default=None, null=True, unique=True, verbose_name='ID сообщения')),
                ('text', models.TextField(blank=True, null=True)),
                ('is_read', models.BooleanField(default=False, verbose_name='Прочтено')),
                ('sender', models.CharField(choices=[('user', 'Пользователь'), ('bot', 'Бот')], max_length=20)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='bot.chat', verbose_name='Переписка с пользователем')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FileId',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=50)),
                ('value', models.CharField(max_length=50)),
            ],
            options={
                'unique_together': {('key', 'value')},
            },
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='chat', to='bot.tguser', verbose_name='Чат с пользователем'),
        ),
        migrations.CreateModel(
            name='BuyerInquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inquiries', to='bot.buyer')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.property', verbose_name='Недвижимость')),
            ],
            options={
                'verbose_name': 'Запрос клиента',
                'verbose_name_plural': 'Запросы клиентов',
            },
        ),
        migrations.AddField(
            model_name='buyer',
            name='customer',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='bot.tguser', verbose_name='Пользователь'),
        ),
    ]