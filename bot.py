import asyncio
import os
from aiogram import Bot

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def on_startup(bot: Bot):
    from bot.config import scheduler
    from bot.misc.set_bot_commands import set_commands
    from bot.misc.mailing import send_mailing
    from bot.services.property_manager import property_manager

    await set_commands(bot)
    await property_manager.update_properties()
    scheduler.add_job(send_mailing, "cron", minute="*",
                      hour="*", args=(bot,))
    scheduler.start()


async def main():

    from bot.config import dp, bot
    from bot.handlers import main_segregations
    main_segregations.register_handlers(dp)

    try:
        await on_startup(bot)
        await dp.start_polling(
            bot,
        )
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
