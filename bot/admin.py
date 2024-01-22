from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe
from asgiref.sync import async_to_sync

from package.utils.update_file import update_property_file

from .models import Client, FileId, Notification, TgUser, Chat, BuyerInquiry, Property


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


class BuyerInquiryInline(admin.TabularInline):
    model = BuyerInquiry
    extra = 0


@admin.register(Client)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'phone_number')
    inlines = (BuyerInquiryInline,)


@admin.register(BuyerInquiry)
class BuyerInquiryAdmin(admin.ModelAdmin):
    list_display = ('customer', 'property')


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'realty_type', 'formated_price')
    search_fields = ('id', 'realty_type', 'city')

    filter_list = ('realty_type',)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('buyer_inquiry', 'text', 'mail_date', 'is_sended')


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
        return chat.user.pk

    @staticmethod
    def link(chat):
        href = reverse('panel:chat', kwargs={'chat_id': chat.user.id})
        return mark_safe(f'<a href="{href}">Перейти к переписке</a>')


@admin.register(TgUser)
class TgUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username',)
    readonly_fields = ('url', 'username')


@admin.register(FileId)
class FileIdAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
