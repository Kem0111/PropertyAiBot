import asyncio
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from amplitude import BaseEvent
from loguru import logger
from openai.error import APIConnectionError, RateLimitError, Timeout, APIError, ServiceUnavailableError, \
    InvalidRequestError
from telebot import TeleBot, types

from admin_panel.telebot.models import Client
from tgbot.keyboards.inline import chat_kb, arrange_subscribe_kb
from tgbot.models.db_commands import get_close_dialog_user, create_dialog, get_user_disabled, get_all_users


async def close_dialog(bot, storage):
    users = await get_close_dialog_user()
    for user in users:
        user.close_session = None
        user.save()
        user.dialog.all().delete()
        need_key = StorageKey(bot_id=bot.id, chat_id=user.telegram_id, user_id=user.telegram_id)
        need_context = FSMContext(bot=bot, storage=storage, key=need_key)
        await need_context.set_state(None)
        try:
            await bot.send_message(text='\n'.join([
                f'🤖 Ваш диалог с ботом завершен. Поскольку вы не проявляли активность более 5 минут.\n',
                f'Введите свой новый вопрос ниже 👇'
            ]),
                reply_markup=await chat_kb(),
                chat_id=user.telegram_id)
        except TelegramForbiddenError:
            pass


async def answer_chat_gpt(user, bot: TeleBot, openai, question):
    logger.info(f'Открыл сессию для [ID: {user.telegram_id}]')
    user = Client.objects.get(pk=user.pk)
    message = bot.send_message(chat_id=user.telegram_id, text="Обрабатываю ответ....")
    dialogs = user.dialog.all()
    if len(dialogs) == 5:
        user.dialog.all().delete()
        dialogs = []
    elif len(dialogs) == 4:
        bot.send_message(chat_id=user.telegram_id, text="❗️Вы достигли лимит в 5 вопросов в "
                                                        "течение одной диалоговой сессии, следующий вопрос "
                                                        "будет отправлен как новый")
    messages = []
    for dialog in dialogs:
        messages.append({"role": "user", "content": dialog.question})
        messages.append({"role": "assistant", "content": dialog.answer})
    messages.append({"role": "user", "content": question})
    model = "gpt-3.5-turbo"
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=messages
        )
        response = completion.choices[0].message.content
    except (APIConnectionError, RateLimitError):
        return bot.edit_message_text(chat_id=user.telegram_id,
                                     text="🚫 Произошла ошибка при подключении к серверам повторите свой вопрос позже",
                                     message_id=message.message_id)
    except (APIError, ServiceUnavailableError, Timeout):
        return bot.edit_message_text(chat_id=user.telegram_id,
                                     text="🚫 Произошла ошибка при подключении к серверам повторите свой вопрос позже",
                                     message_id=message.message_id)
    except InvalidRequestError:
        user.dialog.all().delete()
        return bot.edit_message_text(chat_id=user.telegram_id,
                                     text="🚫 Ошибка переполнения истории, обновите сессию 👇",
                                     message_id=message.message_id, reply_markup=answer_kb())
    except Exception as e:
        logger.error(f'{type(e).__name__}: {e}')
    try:
        bot.edit_message_text(chat_id=user.telegram_id, text="✅ Ваш ответ готов",
                              message_id=message.message_id)
        user.use_tokens += completion.usage.total_tokens
        if not user.subscribe:
            token_limits = user.token_limits
            if token_limits - completion.usage.total_tokens < 0:
                user.token_limits = 0
            else:
                user.token_limits -= completion.usage.total_tokens
        close_session_time = datetime.now() + timedelta(minutes=5)
        user.close_session = close_session_time
        user.save()
        parts = [response[i:i + 4096] for i in range(0, len(response), 4096)]
        for part in parts:
            bot.send_message(chat_id=user.telegram_id, text=part, reply_markup=answer_kb())
        await create_dialog(user, question, response)
    except Exception as e:
        logger.error(f'{type(e).__name__}: {e}')
    logger.info(f'Закрыл сессию для [ID: {user.telegram_id}]')


async def unsubscribe_user(bot: Bot):
    users = await get_user_disabled()
    for user in users:
        try:
            await bot.send_message(chat_id=user.telegram_id, text='\n'.join([
                f'Ваша подписка закончилась',
                f'Доступ к боту приостановлен\n',
                f'Для продления подписки нажмите на кнопку ниже 👇',
            ]), reply_markup=await arrange_subscribe_kb())
        except TelegramForbiddenError:
            logger.info(
                f'Ошибка при отправке сообщения пользователю [ID: {user.telegram_id}], пользователь заблокировал бота')
        user.end_subscribe = None
        user.subscribe = False
        user.save()
        logger.info(
            f'Подписка для пользователя @{user.username} [ID: {user.telegram_id}] была отключена по истечению времени')


def answer_kb():
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("🔄 Другой вопрос", callback_data="refresh_session")
    markup.add(button1)
    return markup


async def analytics(event, amplitude, user_id, username):
    amplitude.track(
        BaseEvent(
            event_type=event,
            user_id=str(user_id),
            device_id=username,
            event_properties={
                "source": "notification"
            }
        )
    )


async def mailing(bot: Bot, text, file_id, media_type):
    users = await get_all_users()
    send_count = 0
    for user in users:
        try:
            if media_type == "no_media":
                await bot.send_message(text=text, chat_id=user.telegram_id)
            elif media_type == "photo":
                await bot.send_photo(caption=text, chat_id=user.telegram_id, photo=file_id)
            elif media_type == "video":
                await bot.send_video(caption=text, chat_id=user.telegram_id, video=file_id)
            elif media_type == "document":
                await bot.send_document(caption=text, chat_id=user.telegram_id, document=file_id)
            send_count += 1
        except (TelegramForbiddenError, TelegramBadRequest):
            continue

        await asyncio.sleep(0.1)
    return send_count




class CreatedModel(models.Model):
    """Абстрактная модель. Добавляет дату создания."""
    created = models.DateTimeField(
        'Дата создания',
        auto_now_add=True
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата изменения")

    class Meta:
        abstract = True


class Client(CreatedModel):
    username = models.CharField(
        max_length=50,
        help_text='Юзернейм клиента',
        verbose_name='Юзернейм',
        blank=True,
        null=True
    )
    telegram_id = models.BigIntegerField(
        help_text='Telegram ID пользователя',
        verbose_name='Telegram ID'
    )
    close_session = models.DateTimeField(
        blank=True,
        null=True
    )
    token_limits = models.IntegerField(
        default=6000,
        help_text='Лимит бесплатной подписки',
        verbose_name='Лимит'
    )
    subscribe = models.BooleanField(
        default=False,
        help_text='Подписка на бота',
        verbose_name='Подписка'
    )
    use_tokens = models.IntegerField(
        default=0,
        help_text='Использование токенов',
        verbose_name='Использование токенов'
    )
    end_subscribe = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Дата окончания подписки',
        verbose_name='Дата окончания подписки'
    )

    class Meta:
        verbose_name = 'Клиенты телеграмм бота'
        verbose_name_plural = 'Клиенты телеграмм бота'
        ordering = ('-created',)

    def __str__(self):
        return self.username


class Dialog(CreatedModel):
    question = models.CharField(
        max_length=8000,
        verbose_name='Вопрос',
        help_text='Вопрос'
    )
    answer = models.CharField(
        max_length=8000,
        verbose_name='Ответ',
        help_text='Ответ',
    )
    user = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='dialog',
        help_text='Пользователь который создал диалог',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Диалог пользователя'
        verbose_name_plural = 'Диалог телеграмм бота'
        ordering = ('created',)


class Referral(models.Model):
    utm_code = models.CharField(
        max_length=100
    )
    count_click = models.IntegerField(
        default=0
    )

    def __str__(self):
        return self.utm_code


class UserReferral(models.Model):
    user = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name='referrals',
        help_text='Пользователь который пригласил',
        verbose_name='Пользователь'
    )
    invited = models.ForeignKey(
        Client,
        on_delete=models.SET_NULL,
        related_name='invited',
        blank=True,
        null=True,
        help_text='Пользователь которого пригласили',
        verbose_name='Приглашенный пользователь'
    )

    class Meta:
        verbose_name = 'Рефералы'
        verbose_name_plural = 'Рефералы'

    def __str__(self):
        return self.user

