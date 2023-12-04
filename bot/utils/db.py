from bot.models import TgUser


async def save_user_data(user: TgUser, user_data):

    await TgUser.objects.filter(
        id=user.id).aupdate(
              full_name=user_data.get('full_name'),
              phone_number=user_data.get('phone_number'),
              email=user_data.get('email')
        )
