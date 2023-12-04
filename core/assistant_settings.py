from bot.config import assistant_manager, openai_client
from bot.services.db_manager import db_manager
from openai import NotFoundError, BadRequestError
import os
from dotenv import load_dotenv


load_dotenv()


class AssistantSettings:
    TOOLS = [
        {"type": "retrieval"},
        {
            "type": "function",
            "function": {
                "name": "determine_user_role",
                "description": "Determine the user's role as either a buyer or an owner.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "role": {
                            "type": "string",
                            "description": "User's response to the question about their role, e.g. buyer"
                        }
                    },
                    "required": ["role"]
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "collect_user_info",
                "description": "Collect user's information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "full_name": {
                            "type": "string",
                            "description": "User's name, e.g. Михаил"
                        },
                        "phone_number": {
                            "type": "string",
                            "description": "User's phone number, e.g. 89857233621"
                        },
                        "email": {
                            "type": "string",
                            "description": "User's email, e.g. test@tes.com"
                        }
                    },
                }
            }
        },
        {
            "type": "function",
            "function": {
                "name": "provide_property_ids",
                "description": "Provide a list of property IDs liked by user.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "property_ids": {
                            "type": "array",
                            "items": {
                                "type": "integer"
                            },
                            "description": "List of property IDs liked by user."
                        }
                    },
                    "required": ["property_ids"]
                }
            }
        }
    ]

    ASSISTANT_NAME = os.getenv("ASSISTANT_NAME")
    assistant_id = os.getenv("ASSISTENT_ID", None)
    MODEL = "gpt-4-1106-preview"
    FILE_PROPERTY_KEY = "FILE_PROPERTY_ID"
    FILE_DIALOGUE_KEY = "FILE_DIALOGUE_ID"

    def get_instructions(self):
        with open('instructions.txt') as file:
            assistant_instructions = file.read()
        return assistant_instructions

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

    async def create_dialogue_file(self):
        return await self._file_proccess(
            self.FILE_DIALOGUE_KEY, "dialogue.txt"
        )

    async def create_properties_file(self):
        return await self._file_proccess(
            self.FILE_PROPERTY_KEY, "properties.json"
        )

    async def create_assistant(self):

        if self.assistant_id:
            await assistant_manager.delete_assistant(self.assistant_id)

        open_ai_property_file_id = await self.create_properties_file()
        open_ai_dialogue_file_id = await self.create_dialogue_file()

        assistant = await assistant_manager.create_assistant(
            name=self.ASSISTANT_NAME,
            instructions=self.get_instructions(),
            tools=self.TOOLS,
            model=self.MODEL,
            file_ids=[open_ai_property_file_id, open_ai_dialogue_file_id]
        )
        self.write_assistant_id_to_env(assistant.id)

    def write_assistant_id_to_env(self, assistant_id):
        # Считывание текущего содержимого .env файла
        with open('.env', 'r') as file:
            lines = file.readlines()

        # Проверка и обновление файла
        assistant_id_found = False
        for i in range(len(lines)):
            if lines[i].startswith('ASSISTENT_ID='):
                lines[i] = f'ASSISTENT_ID={assistant_id}\n'
                assistant_id_found = True
                break

        # Добавление ASSISTENT_ID, если он не найден
        if not assistant_id_found:
            lines.append(f'ASSISTENT_ID={assistant_id}\n')

        # Перезапись файла .env с обновленными данными
        with open('.env', 'w') as file:
            file.writelines(lines)


assistant = AssistantSettings()
