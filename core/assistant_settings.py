from bot.config import assistant_manager, openai_client
from bot.models import FileId
from bot.services.db_manager import db_manager
from openai import NotFoundError, BadRequestError
from package.settings import ASSISTENT_NAME, FILE_INSTRUCTION_PATH, FILE_INSTRUCTION_ID
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
                "description": "This function is designed to collect user information. It takes user input such as full name, phone number, and email address, and returns them in a structured format. During processing, the function removes all extraneous whitespace characters, including new lines, and validates the data against specific formats (e.g., phone number and email formats). This ensures the accuracy and consistency of the returned data and prevents potential errors when saving the data in a database later",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "full_name": {
                            "type": "string",
                            "description": "A string containing the user's full name. The function automatically trims leading and trailing spaces, as well as any other whitespace characters, including new lines e.g. Михаил"
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
        },
        {
            "type": "function",
            "function": {
                "name": "search_and_provide_properties",
                "description": "Search properties based on user preferences",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price": {
                            "type": "number",
                            "description": "price for the property search"
                        },
                        "room_count": {
                            "type": "number",
                            "description": "room count for the property search"
                        },
                        "area": {
                            "type": "number",
                            "description": "area of the property in square meters"
                        },
                        "district": {
                            "type": "string",
                            "description": "Preferred district for the property e.g., Печерский"
                        },
                        "city": {
                            "type": "string",
                            "description": "Preferred city for the property, e.g., Киев, Киево-Святошинский"
                        },
                        "realty_type": {
                            "type": "string",
                            "description": "Type of the realty, only one of this items: квартира, частный дом, офисное помещение, коммерческое помещение, участок под жилую застройку, земля сельскохозяйственного назначения, земля коммерческого назначения, коммерческое помещение"
                        },
                        "street": {
                            "type": "string",
                            "description": "Preferred street or location, e.g., Драгомирова"
                        },
                        "advert_type": {
                            "type": "string",
                            "description": "Type of advertisement, only one of this items:, продажа, долгосрочная аренда"
                        },
                        "page_number": {
                            "type": "number",
                            "description": "Specifies the page number of the search results to be displayed. Used for pagination to navigate through different sets of results"
                        }
                    },
                    "required": ["advert_type", "realty_type", "city", "page_number"]
                }
            }
        }

    ]

    MODEL = "gpt-4-1106-preview"
    DESCRIPTION = "Property Bot"
    INSTRUCTION = "Все инструкции в переданном файле детально его изучи"

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

        open_ai_instruct_file_id = await self.create_instruct_file()

        assistant = await assistant_manager.create_assistant(
            name=ASSISTENT_NAME,
            description=self.DESCRIPTION,
            instructions=self.INSTRUCTION,
            tools=self.TOOLS,
            model=self.MODEL,
            file_ids=[open_ai_instruct_file_id]
        )
        await db_manager.update_assistant_id(assistant.id)


assistant = AssistantSettings()
