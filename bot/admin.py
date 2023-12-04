from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from asgiref.sync import async_to_sync
import csv

from package.utils.update_file import update_property_file

from .models import TgUser, Buyer, Owner, Chat, BuyerInquiry, Property


def update_csv_file():
    properties = Property.objects.filter(is_passed=False).all()
    with open('properties.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            'ID', 'Название', 'Детали', 'Цена', 'Валюта', 'Локация'
        ])
        for prop in properties:
            writer.writerow(
                [
                    prop.id, prop.title, prop.details, prop.price,
                    prop.currency, prop.location
                ]
            )


# Register your models here.
class User(DefaultUser):

    class Meta:
        proxy = True
        verbose_name = 'Администратора'
        verbose_name_plural = 'Администраторы сайта'


admin.site.unregister(DefaultUser)


@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    pass


@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ('customer',)


class BuyerInquiryInline(admin.TabularInline):
    model = BuyerInquiry
    extra = 0


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('customer',)
    inlines = (BuyerInquiryInline,)


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'location', 'formated_price')
    search_fields = ('id', 'type', 'location')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        update_csv_file()  # Обновление CSV файла после сохранения модели
        async_to_sync(update_property_file)()

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
        update_csv_file()
        async_to_sync(update_property_file)()


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        'username', 'get_user_name',
        'link', 'count_unread', 'last_message_created'
    )
    readonly_fields = ('user', 'count_unread', 'last_message_created',)

    ordering = ['-last_message_created']

    @staticmethod
    def username(chat):
        return chat.user.username

    @staticmethod
    def full_name(chat):
        return chat.user.full_name

    @staticmethod
    def link(chat):
        href = reverse('panel:chat', kwargs={'chat_id': chat.user.id})
        return mark_safe(f'<a href="{href}">Перейти к переписке</a>')


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'full_name', 'email')
    readonly_fields = ('url', 'username', 'email', 'full_name', 'id', 'phone_number')
