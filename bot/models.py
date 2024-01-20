
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

    REALTY_TYPE_CHOICES = (
        ('квартира', 'квартира'),
        ("земля коммерческого назначения", "земля коммерческого назначения"),
        ("земля сельскохозяйственного назначения", "земля сельскохозяйственного назначения"),
        ("участок под жилую застройку", "участок под жилую застройку"),
        ("частный дом", "частный дом"),
        ("офисное помещение", "офисное помещение"),
        ("коммерческое помещение", "коммерческое помещение"),
    )

    ADVERT_TYPE_CHOICES = (
        ('продажа', 'продажа'),
        ('долгосрочная аренда', 'долгосрочная аренда'),
    )

    PRICE_TYPE_CHOICES = (
        ('за объект', 'за объект'),
        ('за участок', 'за участок'),
        ('за кв.м.', 'за кв.м.'),
    )

    WALL_TYPE_CHOICES = (
        ('кирпич', 'Кирпич'),
    )

    HEATING_TYPE_CHOICES = (
        ('централизованное', 'централизованное'),
        ('индивидуальное', 'индивидуальное'),
    )
    STREET_TYPE_CHOICES = (
        ("улица", "улица"),
        ("шоссе", "шоссе"),
        ("бульвар", "бульвар"),
        ("площадь", "площадь"),
        ("переулок", "переулок"),
        ("проспект", "проспект")
    )
    FLAT_STATE_CHOICES = (
        ("без отделочных работ", "без отделочных работ"),
        ("черновые работы / строительная отделка", "черновые работы / строительная отделка"),
        ("аварийное", "аварийное"),
        ("евроремонт", "евроремонт"),
        ("дизайнерский ремонт", "дизайнерский ремонт"),
        ("косметический ремонт", "косметический ремонт"),
        ("удовлетворительное", "удовлетворительное")
    )
    realty_type = models.CharField(max_length=50, choices=REALTY_TYPE_CHOICES, verbose_name='Тип недвижимости')
    advert_type = models.CharField(max_length=50, choices=ADVERT_TYPE_CHOICES, verbose_name='Тип объявления')
    state = models.CharField(max_length=100, verbose_name='Область')
    city = models.CharField(max_length=100, verbose_name='Город')
    district = models.CharField(max_length=100, verbose_name='Район', null=True)
    street = models.CharField(max_length=100, verbose_name='Улица', null=True)
    street_type = models.CharField(max_length=50, choices=STREET_TYPE_CHOICES, verbose_name='Тип улицы')
    building_number = models.CharField(max_length=10, verbose_name='Номер здания', null=True)
    description = models.TextField(verbose_name='Описание', null=True)
    # Characteristics
    rooms_count = models.IntegerField(verbose_name='Количество комнат', null=True)
    total_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Общая площадь', null=True)
    living_area = models.DecimalField(max_digits=6, decimal_places=2, verbose_name='Жилая площадь', null=True)
    kitchen_area = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Площадь кухни', null=True)
    floor = models.IntegerField(verbose_name='Этаж', null=True)
    floors = models.IntegerField(verbose_name='Количество этажей', null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    price_type = models.CharField(max_length=50, choices=PRICE_TYPE_CHOICES, verbose_name='Тип цены', null=True)
    currency = models.CharField(max_length=10, verbose_name='Валюта')
    build_year = models.CharField(max_length=50, verbose_name='Год постройки', null=True)
    flat_state = models.CharField(max_length=100, choices=FLAT_STATE_CHOICES ,verbose_name='Состояние квартиры', null=True)
    wall_type = models.CharField(max_length=50, choices=WALL_TYPE_CHOICES, verbose_name='Тип стен', null=True)
    heating = models.CharField(max_length=50, choices=HEATING_TYPE_CHOICES, verbose_name='Тип отопления', null=True)

    def __str__(self):
        return f"{self.realty_type} {self.pk}"

    class Meta:
        verbose_name = 'Недвижимость'
        verbose_name_plural = 'Недвижимость'
        ordering = ['id']

    def formated_price(self):
        return f"{self.price} {self.currency}"
    formated_price.short_description = 'Цена'

    def formatted_price(self):
        return f"{self.price} {self.currency}"

    def full_address(self):
        address_parts = [self.city, self.district, self.street_type, self.street, self.building_number]
        # Удаляем пустые части адреса
        address_parts = [part for part in address_parts if part]
        return ", ".join(address_parts)

    def get_detail_if_true(self, title, field):
        return f'{title}: {field}' if field else ''

    def get_main_details(self):
        rooms_count = self.get_detail_if_true('Количество комнат', self.rooms_count)
        living_area = self.get_detail_if_true('Жилая площадь', self.living_area)
        kitchen_area = self.get_detail_if_true('Площадь кухни', self.kitchen_area)
        floor = self.get_detail_if_true('Этаж', self.floor)
        floors = self.get_detail_if_true('Количество этажей', self.floors)
        flat_state = self.get_detail_if_true('Состояние квартиры', self.flat_state)
        wall_type = self.get_detail_if_true('Тип стен', self.wall_type)
        heating = self.get_detail_if_true('Тип отопления', self.heating)
        return f"{rooms_count}\n{living_area}\n{kitchen_area}\n{floor}\n{floors}\n{flat_state}\n{wall_type}\n{heating}\n"

    def detailed_description(self):
        return (
            f"""ID: {self.pk}\n\n{self.realty_type},\n
            {self.advert_type} в {self.full_address()}.\n
            Цена: {self.formatted_price()}.\n
            {self.get_main_details()}\n
            Описание: {self.description}"""
        )


class PropertyPhoto(models.Model):
    property = models.ForeignKey(Property, related_name='photos', on_delete=models.CASCADE, verbose_name='Недвижимость')
    photo_url = models.URLField(verbose_name='URL фотографии')

    def __str__(self):
        return f"Фотография для {self.property}"

    class Meta:
        verbose_name = 'Фотография недвижимости'
        verbose_name_plural = 'Фотографии недвижимости'


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
