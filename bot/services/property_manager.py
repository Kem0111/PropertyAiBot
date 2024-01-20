import aiohttp
from .xml_parser import parse_and_update_database


class PropertyManager:
    PROPERTY_URL = "https://crm-primes.realtsoft.net/feed/xml?id=2"

    async def fetch_xml(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                xml_data = await response.text()
                xml_data = xml_data.replace('xmlns="https://dom.ria.com/xml/xsd/"', '')
                return xml_data

    async def update_properties(self):
        xml_data = await self.fetch_xml(self.PROPERTY_URL)
        await parse_and_update_database(xml_data)


property_manager = PropertyManager()
