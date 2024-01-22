from bot.models import TgUser, BuyerInquiry
from asgiref.sync import sync_to_async


async def save_user_data(user: TgUser, user_data):

    await TgUser.objects.filter(
        id=user.id).aupdate(
              full_name=user_data.get('full_name'),
              phone_number=user_data.get('phone_number'),
              email=user_data.get('email')
        )


async def get_orders(start_index: int,
                     end_index: int,
                     *args,
                     **kwargs):
    orders = await sync_to_async(list)(
        BuyerInquiry.objects.filter(
            **kwargs
        ).order_by('-created')[start_index:end_index]
    )
    total = await BuyerInquiry.objects.filter(**kwargs).acount()
    return orders, total
