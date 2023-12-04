
import asyncio
import os
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def main():
    from core.assistant_settings import assistant

    await assistant.create_assistant()


if __name__ == "__main__":
    asyncio.run(main())
