from package.settings import ASSISTENT_ID
from bot.config import assistant_manager
from bot.models import FileId


FILE_PROPERTY_KEY = "FILE_PROPERTY_ID"
FILE_PATH = "properties.csv"


def get_files_ids(changed_file_key):

    files = FileId.objects.all()
    return [file.value for file in files if file.key != changed_file_key]


async def update_property_file():

    file_property = await FileId.objects.filter(
        key="FILE_PROPERTY_ID"
    ).afirst()
    file_ids = get_files_ids(FILE_PROPERTY_KEY)

    await assistant_manager.update_assistant_file(
        ASSISTENT_ID, file_property.value, FILE_PATH, FILE_PROPERTY_KEY, file_ids
    )
