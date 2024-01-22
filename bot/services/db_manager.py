from bot.models import Client, FileId, TgUser, BuyerInquiry, Notification
from package.settings import ASSISTENT_ID_KEY
from asgiref.sync import sync_to_async


class DbManager:

    async def update_user_info(self, user_id, **kwargs):
        await TgUser.objects.aupdate_or_create(id=user_id, defaults=kwargs)

    async def client_proccess(self, user_id, **kwargs):
        property_id = kwargs.pop("property_id")
        full_name = kwargs.get('full_name').strip()
        phone_number = kwargs.get('phone_number').strip()
        email = kwargs.get('email').strip()
        client, _ = await Client.objects.aget_or_create(
            full_name=full_name,
            phone_number=phone_number or None,
            email=email or None
        )

        await BuyerInquiry.objects.acreate(
            user_id=user_id,
            property_id=property_id,
            customer_id=client.pk
        )

    async def add_notification(self, user_id,  **kwargs):
        await Notification.objects.acreate(
            user_id=user_id,
            **kwargs
        )

    async def get_assistant_id(self):
        assistant = await FileId.objects.filter(key=ASSISTENT_ID_KEY).afirst()
        return assistant.value if assistant else None

    async def update_assistant_id(self, assistant_id):
        await FileId.objects.aupdate_or_create(key=ASSISTENT_ID_KEY, defaults={"value": assistant_id})

    async def get_file_id(self, key):
        openai_file = await FileId.objects.filter(key=key).afirst()
        return openai_file

    async def get_buyer_inquiry(self, order_id):
        order = await BuyerInquiry.objects.filter(id=order_id).afirst()
        return await sync_to_async(order.stringify)()

    async def save_file_id(self, file_id: str, key: str) -> None:

        await FileId.objects.aupdate_or_create(
            key=key,
            defaults={
                "value": file_id
            }
        )


db_manager = DbManager()
