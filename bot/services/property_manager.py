# import aiohttp
# import aiofiles
# from bot.utils.update_file import update_property_file
# from .xml_parser import parse_and_update_database
# from package.settings import PROPERTY_FILE_PATH
# import xml.etree.ElementTree as ET
# import json
# import xmltodict


# class PropertyManager:
#     PROPERTY_URL = "https://crm-primes.realtsoft.net/feed/xml?id=2"

#     async def fetch_xml(self, url):
#         async with aiohttp.ClientSession() as session:
#             async with session.get(url) as response:
#                 xml_data = await response.text()
#                 xml_data = xml_data.replace('xmlns="https://dom.ria.com/xml/xsd/"', '')
#                 return xml_data

#     # async def save_file(self, file_path, xml_data):
#     #     xpars = xmltodict.parse(xml_data)
#     #     json_data = json.dumps(xpars['realties']['realty'], indent=4, ensure_ascii=False)
#     #     async with aiofiles.open(file_path, mode='w', encoding='utf-8') as file:
#     #         await file.write(json_data)

#     async def update_openai_property_file(self):
#         await update_property_file()

#     async def update_properties(self):
#         xml_data = await self.fetch_xml(self.PROPERTY_URL)
#         # await self.save_file(PROPERTY_FILE_PATH, xml_data)
#         await parse_and_update_database(xml_data)
#         # await self.update_openai_property_file()


# property_manager = PropertyManager()
