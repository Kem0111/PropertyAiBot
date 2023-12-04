import requests
import json

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from dotenv import load_dotenv

from .models import Message, Chat
from package.settings import BOT_TOKEN

load_dotenv()


@login_required
def view_chat(request, chat_id):
    chat = get_object_or_404(Chat, user__id=chat_id)
    if request.method == 'POST':
        text = request.POST.get('message_text')

        data = {
            'chat_id': chat_id,
            'text': text
        }

        url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
        response = requests.post(url, data=data)
        data = json.loads(response.text)
        if response.status_code == 200:
            Message.objects.create(
                message_id=data['result']['message_id'],
                text=text,
                sender='bot',
                chat=chat,
                is_read=True,
            )

        return redirect(request.path)

    messages_list = chat.messages.all()
    chat.count_unread = 0
    chat.save()

    all_chats = Chat.objects.all()

    template = 'tgbot/chat.html'
    return render(request, template, {
        'messages_list': messages_list,
        'chat_id': chat_id,
        'chats_list': all_chats
    })


def get_updated_data(request, chat_id):
    chat = get_object_or_404(Chat, user__id=chat_id)
    if chat.count_unread > 0:
        messages_list = [
            {
                'text': message.text,
                'sender': message.sender,
                'chat': {
                    'user': {
                        'url': message.chat.user.url,
                        'full_name': message.chat.user.username,
                    }
                },
                'created': message.created
            }
            for message in list(chat.messages.filter())[-chat.count_unread:]
        ]

        chat.count_unread = 0
        chat.save()

        data = {'messages_list': messages_list}
    else:
        data = {}
    return JsonResponse(data)


def get_updated_all_chats_data(request):
    from django.urls import reverse

    chats = Chat.objects.all()
    chats_list = [
        {
            'user': {
                'id': chat.user.id,
                'full_name': chat.user.username
            },
            'link': reverse("panel:chat", kwargs={"chat_id": chat.user.id}),
            'count_unread': chat.count_unread,
        }
        for chat in chats
    ]
    data = {'chats_list': chats_list}
    return JsonResponse(data)
