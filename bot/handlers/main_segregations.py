from typing import Union
from aiogram import F, types, Dispatcher
from aiogram.fsm.context import FSMContext
from bot.keyboards.pagination_kb import generate_db_items_keyboard
from bot.models import UserThread
from django.core.exceptions import ObjectDoesNotExist
from bot.config import thread_manager, assistant_manager, bot, texts
from bot.services.db_manager import db_manager
from bot.utils.db import get_orders
from bot.utils.fabrics import create_page_hanler
from bot.services.chat_session import ChatSession
from aiogram.filters import Command


assistan_id = None


async def order_cmd_handler(message: Union[types.Message, types.CallbackQuery],
                            page: int = 0):
    msg = message.message if isinstance(message, types.CallbackQuery) else message

    orders = await generate_db_items_keyboard(
        page,
        get_orders,
        'view_orders',
        'back_to_main_menu',
        'view_list_order',
        user_id=message.from_user.id,
    )

    try:
        await msg.edit_text(text=texts['start'], reply_markup=orders.as_markup())
    except Exception:
        await msg.answer(text=texts['start'], reply_markup=orders.as_markup())

ORDER_VIEW_PAGINATION_GROUP = {
    'page_view_list_order': order_cmd_handler
}

user_view_pagination_hendler = create_page_hanler(
    ORDER_VIEW_PAGINATION_GROUP
)


async def order_details(call: types.CallbackQuery):
    order_id = int(call.data.split()[1])
    order_text = await db_manager.get_buyer_inquiry(order_id)
    current_markup = call.message.reply_markup

    await call.message.edit_text(
        text=order_text,
        reply_markup=current_markup
    )


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
    dp.message.register(order_cmd_handler, Command('orders'))
    dp.message.register(on_start)
    dp.callback_query.register(
        user_view_pagination_hendler,
        F.data.startswith('page_view_list_order')
    )
    dp.callback_query.register(
        order_details,
        F.data.startswith('view_orders')
    )
    dp.message.register(on_start)
