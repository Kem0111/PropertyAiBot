from package.settings import ASSISTENT_ID
import os
import django
import asyncio

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "package.settings")
django.setup()


async def update_assistant():
    from bot.config import assistant_manager, openai_client
    from bot.models import FileId

    

    with open('instructions.txt') as file:
        assistant_instructions = file.read()

    await assistant_manager.update_assistant(
        ASSISTENT_ID,
        instructions=assistant_instructions,
        tools=tools
    )

if __name__ == "__main__":
    asyncio.run(update_assistant())
