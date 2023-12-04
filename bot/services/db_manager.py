from bot.models import FileId, TgUser, Buyer, Owner, BuyerInquiry
from django.db.models import Model
from django.db.utils import IntegrityError


class DbManager:

    ROLE = {
        "buyer": Buyer,
        "owner": Owner
    }

    async def update_user_info(self, user_id, **kwargs):
        await TgUser.objects.aupdate_or_create(id=user_id, defaults=kwargs)

    async def add_user_role(self, user_id, role="owner"):
        model: Model = self.ROLE.get(role)

        await model.objects.aget_or_create(
            customer_id=user_id
        )

    async def add_user_request_pr(self, user_id, property_ids=[]):
        customer, _ = await Buyer.objects.aget_or_create(customer_id=user_id)
        print(property_ids)

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


db_manager = DbManager()
