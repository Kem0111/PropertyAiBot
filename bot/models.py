
from django.db import models


class CreatedModel(models.Model):

    created = models.DateTimeField(
        verbose_name='Дата создания',
        auto_now_add=True
    )

    class Meta:
        abstract = True


# Create your models here.
class TgUser(CreatedModel):
    id = models.BigIntegerField(
        verbose_name='ID пользователя в Telegram',
        primary_key=True
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=255,
        null=True,
        blank=True,
    )
    full_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Полное имя'
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        verbose_name='Номер',
        blank=True,
        null=True,
    )
    email = models.EmailField(
        unique=True,
        verbose_name='Электронная почта',
        blank=True,
        null=True
    )
    url = models.CharField(verbose_name='Ссылка на пользователя', max_length=255, unique=True)
    has_previous_inquiries = models.BooleanField(
        default=False,
        verbose_name='Обращался или нет',
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.username}"

    class Meta:
        verbose_name = 'Телеграм пользователя'
        verbose_name_plural = 'Телеграм пользователи'


class UserThread(models.Model):
    user = models.OneToOneField(
        TgUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    threade = models.CharField(max_length=150, verbose_name='Идентификатор треда')


class Owner(models.Model):
    customer = models.OneToOneField(
        TgUser,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )

    def __str__(self):
        return self.customer.full_name if self.customer.full_name \
            else f"Пользователь {self.customer.id}"

    class Meta:
        verbose_name = 'Собственника'
        verbose_name_plural = 'Собственники'


class Buyer(models.Model):
    customer = models.OneToOneField(
        TgUser, on_delete=models.CASCADE, verbose_name='Пользователь')

    def __str__(self):
        return self.customer.full_name or self.customer.username

    class Meta:
        verbose_name = 'Покупателя'
        verbose_name_plural = 'Покупатели'


class Property(CreatedModel):
    type = models.CharField(verbose_name='Тип обьекта')
    details = models.TextField(verbose_name='Описание обьекта')
    location = models.CharField(max_length=100, verbose_name='Местоположение')
    price = models.DecimalField(max_digits=10, decimal_places=2,
                                verbose_name='Цена')
    currency = models.CharField(max_length=9,
                                verbose_name='Валюта')
    is_passed = models.BooleanField(default=False, verbose_name='Сдан?')

    def __str__(self) -> str:
        return f"{self.type} на {self.location}"

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'
        ordering = ['created']

    def formated_price(self):
        return f"{self.price} {self.currency}"
    formated_price.short_description = 'Цена'


class BuyerInquiry(CreatedModel):
    customer = models.ForeignKey(Buyer,
                                 on_delete=models.CASCADE,
                                 related_name='inquiries')
    property = models.ForeignKey(Property,
                                 on_delete=models.CASCADE,
                                 verbose_name='Недвижимость')

    def __str__(self):
        return f"Запрос {self.customer} на {self.property}"

    class Meta:
        verbose_name = 'Запрос клиента'
        verbose_name_plural = 'Запросы клиентов'


class Chat(models.Model):
    user = models.OneToOneField(
        TgUser,
        verbose_name='Чат с пользователем',
        related_name='chat',
        on_delete=models.CASCADE
    )
    count_unread = models.PositiveIntegerField(
        verbose_name='Количество непрочитанных сообщений', default=0)
    last_message_created = models.DateTimeField(
        verbose_name='Дата создания последнего сообщения',
        null=True,
        blank=True,
        default=None
    )

    def get_user_name(self):
        return self.user.full_name

    get_user_name.short_description = 'ФИО'

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'
        ordering = ['-count_unread']


class Message(CreatedModel):
    message_id = models.PositiveIntegerField(
        verbose_name='ID сообщения', unique=True, null=True, default=None)
    text = models.TextField(blank=True, null=True)
    chat = models.ForeignKey(
        Chat,
        verbose_name='Переписка с пользователем',
        related_name='messages',
        on_delete=models.CASCADE
    )
    is_read = models.BooleanField(verbose_name='Прочтено', default=False)
    sender = models.CharField(
        max_length=20,
        choices=[
            ('user', 'Пользователь'),
            ('bot', 'Бот'),
        ]
    )


class FileId(models.Model):
    key = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        unique_together = ('key', 'value')
