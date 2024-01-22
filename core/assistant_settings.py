from bot.config import assistant_manager, openai_client
from bot.services.db_manager import db_manager
from openai import NotFoundError, BadRequestError
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from datetime import datetime as dt
from package.settings import (
    ASSISTENT_NAME, FILE_INSTRUCTION_PATH, FILE_INSTRUCTION_ID
)

load_dotenv()


class Notification(BaseModel):
    text: str = Field(..., description='Notification text')
    mail_date: dt = Field(..., description="Notification time in ISO 8601 format, e.g., '2024-03-20T17:35:11.382192'")
    buyer_inquiry_id: int = Field(..., description='ID buyer inquiry e.g. 10 ptional parameter, do not send with the response if no ID is received')


class UserInfo(BaseModel):
    full_name: str = Field(..., description="User's name, e.g. Михаил")
    phone_number: str = Field(..., description="User's phone number, e.g. 89857233621")
    email: str = Field(..., description="User's email, e.g. test@tes.com")
    property_id: int = Field(..., description="property ID, e.g. 1523 Optional parameter, do not send with the response if no ID is received")


class AssistantSettings:
    TOOLS = [
        {"type": "code_interpreter"},
        {
            "type": "function",
            "function": {
                "name": "collect_user_info_for_order",
                "description": "Collect user's information and property id, If some data is missing, then do not send any values for those parameters.",
                "parameters": UserInfo.model_json_schema()
            }
        },
        {
            "type": "function",
            "function": {
                "name": "add_notification",
                "description": "A simple reminder for a specific client property request",
                "parameters": Notification.model_json_schema(),
                    "required": ["text", "mail_date"]
                }
        }
    ]

    MODEL = "gpt-4-1106-preview"
    DESCRIPTION = "Property Bot"
    INSTRUCTION = """
Ты являешься специализированным ботом помощником агентов по недвижимости,
основная задача которого – помочь агентам в формировании и добавлении
пользователей и напоминаний.
Используй функцию collect_user_info_for_order для того что бы зафиксировать
клиента по опроделенному обьекту недвижимости, используй add_notification
что бы помочь агенту поставить уведомления под определенные даты,
соотвественно если тебе говорят напомнить через полгода что-то, то в поле
mail_date ты возвращаешь точную дату для сохранения в базе данных по модели
поля DateTimeField, всегда узнавай точную сегодняшнюю дату через код и от него
расчитай нужную дату, ожидается получение времени
в формате ISO 8601, если время и дата не задано по дефолту ставь через неделю
    """

    async def delete_file(self, file_id):
        try:
            await openai_client.files.delete(file_id)
        except (NotFoundError, BadRequestError):
            pass

    async def _file_proccess(self, key: str, path: str) -> str:
        existing_file = await db_manager.get_file_id(key)
        if existing_file:
            await self.delete_file(existing_file.value)

        open_ai_file = await openai_client.files.create(
            file=open(path, "rb"), purpose='assistants'
        )

        await db_manager.save_file_id(
            open_ai_file.id,
            key
        )
        return open_ai_file.id

    async def create_instruct_file(self):
        return await self._file_proccess(
            FILE_INSTRUCTION_ID, FILE_INSTRUCTION_PATH
        )

    async def create_assistant(self):

        assistant_id = await db_manager.get_assistant_id()

        if assistant_id:
            await assistant_manager.delete_assistant(assistant_id)

        # open_ai_instruct_file_id = await self.create_instruct_file()

        assistant = await assistant_manager.create_assistant(
            name=ASSISTENT_NAME,
            description=self.DESCRIPTION,
            instructions=self.INSTRUCTION,
            tools=self.TOOLS,
            model=self.MODEL,
            # file_ids=[open_ai_instruct_file_id]
        )
        await db_manager.update_assistant_id(assistant.id)


assistant = AssistantSettings()
