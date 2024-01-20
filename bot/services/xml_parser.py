import xml.etree.ElementTree as ET
from bot.models import Property, PropertyPhoto


def get_element_text(element, tag):
    found_element = element.find(tag)
    return found_element.text if found_element is not None else None


async def parse_and_update_database(file_content):

    # Разбор XML-файла
    root = ET.fromstring(file_content)

    for realty in root.findall('realty'):
        # Извлечение основных данных
        local_realty_id = get_element_text(realty, 'local_realty_id')
        realty_type = get_element_text(realty, 'realty_type')
        advert_type = get_element_text(realty, 'advert_type')
        state = get_element_text(realty, 'state')
        city = get_element_text(realty, 'city')
        district = get_element_text(realty, 'district')
        street = get_element_text(realty, 'street')
        street_type = get_element_text(realty, 'street_type')
        building_number = get_element_text(realty, 'building_number')
        description = get_element_text(realty, 'description_uk')

        # Извлечение данных из characteristics
        characteristics = realty.find('characteristics')
        price = get_element_text(characteristics, 'price')
        currency = get_element_text(characteristics, 'currency')
        rooms_count = get_element_text(characteristics, 'rooms_count')
        total_area = get_element_text(characteristics, 'total_area')
        living_area = get_element_text(characteristics, 'living_area')
        kitchen_area = get_element_text(characteristics, 'kitchen_area')
        floor = get_element_text(characteristics, 'floor')
        floors = get_element_text(characteristics, 'floors')
        build_year = get_element_text(characteristics, 'build_year')
        flat_state = get_element_text(characteristics, 'flat_state')
        wall_type = get_element_text(characteristics, 'wall_type')
        heating = get_element_text(characteristics, 'heating')

        # Создание или обновление объекта недвижимости
        property_obj, _ = await Property.objects.aupdate_or_create(
            id=local_realty_id,
            defaults={
                'realty_type': realty_type,
                'advert_type': advert_type,
                'state': state,
                'city': city,
                'district': district,
                'street': street,
                'street_type': street_type,
                'building_number': building_number,
                'description': description,
                'price': price,
                'currency': currency,
                'rooms_count': rooms_count,
                'total_area': total_area,
                'living_area': living_area,
                'kitchen_area': kitchen_area,
                'floor': floor,
                'floors': floors,
                'build_year': build_year,
                'flat_state': flat_state,
                'wall_type': wall_type,
                'heating': heating
            }
        )

        # Извлечение и добавление фотографий
        photos_urls = realty.find('photos_urls')
        if photos_urls:
            for photo_url in photos_urls.findall('loc'):
                await PropertyPhoto.objects.aget_or_create(
                    property=property_obj,
                    photo_url=photo_url.text
                )
