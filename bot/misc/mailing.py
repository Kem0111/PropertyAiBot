from aiogram import Bot, exceptions
from asgiref.sync import sync_to_async
from django.utils import timezone
from aiogram.types.input_file import FSInputFile
from bot.models import Notification, TgUser


async def send_mailing(bot: Bot) -> None:

    now = timezone.now()
    mail = await Notification.objects.filter(mail_date__lte=now, is_sended=False).afirst()
    if mail:
        users = TgUser.objects.filter()
        async for user in users:

            try:
                bot_message = await bot.send_message(user.id, f"<b>Напоминание:</b>\n{mail.text}")
                await bot.pin_chat_message(
                    chat_id=user.id,
                    message_id=bot_message.message_id
                )
            except exceptions.TelegramBadRequest:
                pass
            except Exception as e:
                print(
                    "Произошла ошибка \n\n{} При отправке сообщения пользователю: "
                    "ID {}".format(
                        e, user.id
                    )
                )
        mail.is_sended = True
        await sync_to_async(mail.save)()
