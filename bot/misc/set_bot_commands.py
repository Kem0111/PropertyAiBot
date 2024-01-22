from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command="start",
            description="Запустить бота",
        ),
        BotCommand(
            command="orders",
            description="Заявки",
        )
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
