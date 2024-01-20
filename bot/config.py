from __future__ import annotations

import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from bot.services.assistant_manager import AssistantManager
from bot.services.thread_manager import ThreadManager
from package.settings import BOT_TOKEN
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from openai import AsyncOpenAI
from package.settings import GPT_TOKEN
from bot.middleware.openai_assistant import ChatActionMiddleware


logging.basicConfig(level=logging.INFO)
file_handler = logging.FileHandler('bot.log')

formatter = logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - [%(Levelname)s] - %(name)s (%(filename)s).%(funcName)s(%(Lineno)d) - %(message)s"
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.ERROR)
logging.getLogger().addHandler(file_handler)


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)

dp = Dispatcher(storage=storage)
dp.message.middleware(ChatActionMiddleware())

openai_client = AsyncOpenAI(api_key=GPT_TOKEN)
assistant_manager = AssistantManager(openai_client)
thread_manager = ThreadManager(openai_client)
scheduler = AsyncIOScheduler()
assistant_id = None
