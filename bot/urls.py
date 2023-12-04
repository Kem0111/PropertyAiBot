from django.urls import path

from . import views

app_name = 'tg'

urlpatterns = [
    path('chat/<int:chat_id>/', views.view_chat, name='chat'),
    path(
        'chat/<int:chat_id>/get-updated-data/',
        views.get_updated_data,
        name='get_updated_data'
    ),
    path(
        'chat/updated-chats-data/',
        views.get_updated_all_chats_data,
        name='get_updated_all_chats_data'
    ),
]
