from bot.models import Property, TgUser
from django.db.models import Q
from asgiref.sync import sync_to_async


async def save_user_data(user: TgUser, user_data):

    await TgUser.objects.filter(
        id=user.id).aupdate(
              full_name=user_data.get('full_name').strip(),
              phone_number=user_data.get('phone_number').strip(),
              email=user_data.get('email').strip()
        )


def num_lte_filter(field_name, value):
    if value is not None:
        return Q(**{f'{field_name}__lte': value})
    return Q()


def num_gte_filter(field_name, value):
    if value is not None:
        return Q(**{f'{field_name}__gte': value})
    return Q()


def exact_filter(field_name, value):
    if value is not None:
        return Q(**{f'{field_name}__iexact': value})
    return Q()


def icontain_filter(field_name, value):
    if value is not None:
        return Q(**{f'{field_name}__icontains': value})
    return Q()


PAGE_SIZE = 5


async def search_properties(**kwargs):

    query = Q()
    query &= num_lte_filter('price', kwargs.get('price'))
    query &= num_gte_filter('total_area', kwargs.get('area'))
    query &= num_gte_filter('room_count', kwargs.get('area'))
    query &= exact_filter('district', kwargs.get('district').strip())
    query &= exact_filter('city', kwargs.get('city').strip())
    query &= exact_filter('realty_type', kwargs.get('realty_type').strip())
    query &= icontain_filter('street', kwargs.get('street').strip())
    query &= exact_filter('advert_type', kwargs.get('advert_type').strip())

    total_count = await Property.objects.filter(query).acount()
    total_pages = (total_count + PAGE_SIZE - 1) // PAGE_SIZE

    start_index = (kwargs['page_number'] - 1) * PAGE_SIZE
    properties = await sync_to_async(Property.objects.filter(query)[start_index:start_index + PAGE_SIZE])()

    return properties, total_pages
