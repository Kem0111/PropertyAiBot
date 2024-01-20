from typing import List, Optional
from bot.models import FileId, Property, TgUser, Buyer, Owner, BuyerInquiry
from django.db.models import Model
from django.db.utils import IntegrityError
from bot.utils.db import search_properties

from package.settings import ASSISTENT_ID_KEY


class DbManager:

    ROLE = {
        "buyer": Buyer,
        "owner": Owner
    }

    async def update_user_info(self, user_id, **kwargs):
        print(kwargs)
        await TgUser.objects.aupdate_or_create(id=user_id, defaults=kwargs)

    async def add_user_role(self, user_id, role="owner"):
        model: Model = self.ROLE.get(role)

        try:
            await model.objects.aget_or_create(
                customer_id=user_id
            )
        except AttributeError as e:
            print(e)

    async def add_user_request_pr(self, user_id, property_ids=[]):
        customer, _ = await Buyer.objects.aget_or_create(customer_id=user_id)

        for property_id in property_ids:
            try:
                await BuyerInquiry.objects.aget_or_create(
                    customer_id=customer.pk,
                    property_id=property_id
                )
            except IntegrityError:
                pass

    async def get_file_id(self, key):
        openai_file = await FileId.objects.filter(key=key).afirst()
        return openai_file

    async def save_file_id(self, file_id: str, key: str) -> None:

        await FileId.objects.aupdate_or_create(
            key=key,
            defaults={
                "value": file_id
            }
        )

    async def get_assistant_id(self):
        assistant = await FileId.objects.filter(key=ASSISTENT_ID_KEY).afirst()
        return assistant.value if assistant else None

    async def update_assistant_id(self, assistant_id):
        await FileId.objects.aupdate_or_create(key=ASSISTENT_ID_KEY, defaults={"value": assistant_id})

    async def get_properties(self, kwargs):
        properties = Optional[List[Property]] = await search_properties(**kwargs)
        if not properties:
            return 'Обьектов не найдено'
        results = ''
        for property in properties:
            results += property.detailed_description()
        return results


db_manager = DbManager()
