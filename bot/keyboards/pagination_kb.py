from aiogram.types import (InlineKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from typing import Awaitable
from bot.config import texts


async def generate_db_items_keyboard(page: int,
                                     select_func: Awaitable,
                                     model_name: str,
                                     back_call: str,
                                     unit_name,
                                     *args,
                                     items_per_page: int = 5,
                                     **kwargs
                                     ) -> InlineKeyboardMarkup:
    builder_size = []
    start_index = page * items_per_page
    end_index = start_index + items_per_page

    items, total = await select_func(start_index, end_index, *args, **kwargs)
    builder = InlineKeyboardBuilder()

    for item in items:
        date_str = item.created.strftime('%d.%m.%Y')

        builder.button(
            text=f"ID {item.id} | {texts['date']}: {date_str}",
            callback_data=f"{model_name} {item.id} {page}"
        )
        builder_size.append(1)

    if page > 0 or end_index < total:
        builder_size.append(0)

    if page > 0:
        builder.button(text="<", callback_data=f"page_{unit_name} {page - 1}")
        builder_size[-1] += 1

    if end_index < total:
        builder.button(text=">", callback_data=f"page_{unit_name} {page + 1}")
        builder_size[-1] += 1

    builder.adjust(*builder_size)

    return builder
