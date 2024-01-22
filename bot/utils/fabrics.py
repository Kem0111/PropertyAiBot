from aiogram import types


def create_page_hanler(state_group: dict):
    async def page_handler(call: types.CallbackQuery):

        page = int(call.data.split()[1])
        await state_group[call.data.split()[0]](call, page)
    return page_handler
