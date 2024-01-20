from django.contrib import admin

# Register your models here.

from django.contrib.auth.models import User as DefaultUser
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import TgUser, Buyer, Owner, Chat, BuyerInquiry, Property, FileId


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
    list_display = ('id', 'realty_type', 'city', 'formated_price')
    search_fields = ('id', 'city')
    list_filter = ('realty_type', 'advert_type')


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


@admin.register(FileId)
class FileIdAdmin(admin.ModelAdmin):
    list_display = ('id', 'key', 'value')
