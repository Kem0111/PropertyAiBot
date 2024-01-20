from typing import Union
from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from bot.models import UserThread
from django.core.exceptions import ObjectDoesNotExist
from bot.config import thread_manager, assistant_manager, bot
from bot.services.db_manager import db_manager

from bot.services.chat_session import ChatSession

assistan_id = None


async def on_start(message: Union[types.Message, types.CallbackQuery]):
    global assistan_id
    typing_msg = await message.answer('⏳ Typing...')

    try:
        threade = await UserThread.objects.aget(user_id=message.from_user.id)
        threade_id = threade.threade
    except ObjectDoesNotExist:
        threade = await thread_manager.create_thread()
        threade_id = threade.id

        await UserThread.objects.acreate(
            user_id=message.from_user.id,
            threade=threade_id
        )

    if not assistan_id:
        assistan_id = await db_manager.get_assistant_id()

    chat_manager = ChatSession(
        thread_manager, assistant_manager,
        message.from_user.id, assistan_id, threade_id
    )

    text = await chat_manager.chat_loop(message.text)

    bot_msg = await bot.send_message(
        chat_id=message.from_user.id,
        text=text,
        parse_mode='MARKDOWN'
    )

    await typing_msg.delete()

    return bot_msg


def register_handlers(dp: Dispatcher):
    dp.message.register(on_start)
