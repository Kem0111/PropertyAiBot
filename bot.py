import asyncio
import os

import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def main():

    from bot.config import dp, bot
    from bot.handlers import main_segregations
    main_segregations.register_handlers(dp)
    
    try:
        await dp.start_polling(
            bot,
        )
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
