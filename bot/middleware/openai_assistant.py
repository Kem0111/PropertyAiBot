from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict
from aiogram.types import Message
from aiogram import BaseMiddleware

from bot.models import Chat, TgUser
from bot.models import Message as MessageModel
from django.db import models
from django.utils import timezone


class ChatActionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:

        tg_user, _ = await TgUser.objects.aget_or_create(
            id=event.from_user.id,
            username=event.from_user.username,
            url=event.from_user.url
        )
        chat, _ = await Chat.objects.aget_or_create(user=tg_user)

        if not tg_user.is_manager:
            return

        await MessageModel.objects.acreate(
            message_id=event.message_id,
            text=event.text,
            chat=chat,
            sender='user'
        )
        bot_message: Message = await handler(event, data)

        if bot_message:

            await MessageModel.objects.acreate(
                message_id=bot_message.message_id,
                text=bot_message.text,
                chat=chat,
                sender='bot'
            )
            await Chat.objects.filter(id=chat.id).aupdate(
                count_unread=models.F('count_unread') + 2,
                last_message_created=timezone.now())
