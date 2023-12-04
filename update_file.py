import asyncio
import os
import django
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()

load_dotenv()

FILE_PROPERTY_ID = os.getenv("FILE_PROPERTY_ID")
FILE_NAME = "FILE_PROPERTY_ID"
FILE_PATH = "data.txt"
FILE_IDS = []


async def update_file():
    from bot.config import assistant_manager, ASSISTENT_ID
    
    await assistant_manager.update_assistant_file(
        ASSISTENT_ID, FILE_PROPERTY_ID, FILE_PATH, FILE_NAME, FILE_IDS
    )


if __name__ == "__main__":
    asyncio.run(update_file())
