import asyncio
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def main():

    from bot.config import dp, bot, scheduler
    # from bot.services.property_manager import property_manager
    from bot.handlers import main_segregations
    main_segregations.register_handlers(dp)

    # await property_manager.update_properties()
    # scheduler.add_job(property_manager.update_properties, 'cron', hour=6, minute=0)
    # scheduler.start()

    try:
        await dp.start_polling(
            bot,
        )
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
