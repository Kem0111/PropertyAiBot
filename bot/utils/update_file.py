from bot.config import assistant_manager
from bot.models import FileId
from bot.services.db_manager import db_manager

from asgiref.sync import sync_to_async


# async def get_files_ids(changed_file_key):
#     req_file_keys = [FILE_PROPERTY_KEY, FILE_DIALOGUE_KEY]
#     files = await sync_to_async(FileId.objects.all)()
#     return await sync_to_async(lambda: [file.value for file in files if file.key != changed_file_key and file.key in req_file_keys])()


# async def update_property_file():
#     assistant_id = await db_manager.get_assistant_id()
#     file_property = await FileId.objects.filter(
#         key="FILE_PROPERTY_ID"
#     ).afirst()
#     file_ids = []
#     await assistant_manager.update_assistant_file(
#         assistant_id, file_property.value, PROPERTY_FILE_PATH, FILE_PROPERTY_KEY, file_ids
#     )
