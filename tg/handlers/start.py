import os

from aiogram import Router, F, Bot
from aiogram.filters import Command, ChatMemberUpdatedFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery, \
    FSInputFile, ChatMemberUpdated
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.types import ChatJoinRequest
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, IS_MEMBER
from tg.models import TelegramUser, Wait
from .text import sister_text, brother_text

router = Router()
CHANNEL_ID = -1002378894473
MESSAGE_ID = 20
@router.message(Command("start"))
async def start_command(msg: Message, command: CommandObject, bot: Bot):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
    user.username = msg.from_user.username
    user.first_name = msg.from_user.first_name
    user.last_name = msg.from_user.last_name
    user.save()
    a = command.args if command else None
    if a == "material":
        forwarded  = await bot.forward_message(chat_id=user.user_id, from_chat_id=CHANNEL_ID, message_id=MESSAGE_ID)

        text = (
            "📖 *При должном усердии и дисциплине* с этим материалом Вы научитесь читать Коран по слогам, *инша-Лла́х*.\n\n"
            "💡 *Мы рекомендуем* начать читать Коран только после того, как освоите *правила Таджвида*."
        )
        await bot.send_message(chat_id=user.user_id,text=text,reply_to_message_id=forwarded.message_id, parse_mode="Markdown")
        builder = InlineKeyboardBuilder()
        if user.gender == "M":
            builder.add(InlineKeyboardButton(text="📝 Записаться на уведомление", callback_data="awaiting_brother"))
            await msg.answer(brother_text, parse_mode="Markdown", reply_markup=builder.as_markup())
        elif user.gender == "F":
            builder.add(InlineKeyboardButton(text="Записаться", url="https://t.me/aysha_5663"))
            await msg.answer(sister_text, parse_mode="Markdown", reply_markup=builder.as_markup())
        else:
            text2 = (
                "📚 *Если вы хотите обучаться в группе с опытным Устазом или Устазой, "
                "мы подготовили удобный формат обучения онлайн.*\n\n"
                "👥 В группе вы сможете:\n"
                "• Получать обратную связь от преподавателя в реальном времени\n"
                "• Совместно практиковать чтение Корана\n"
                "• Усваивать правила Таджвида быстрее благодаря групповому взаимодействию\n\n"
                "✨ *Чтобы мы могли подобрать подходящую группу, укажите, пожалуйста, ваш пол:*"
            )
            builder.add(InlineKeyboardButton(text="🤵‍♂️ Я Брат", callback_data="im_brother"))
            builder.add(InlineKeyboardButton(text="🧕 Я Сестра", callback_data="im_sister"))
            builder.adjust(2)
            await msg.answer(text2, reply_markup=builder.as_markup(), parse_mode="Markdown")
    else:
        builder = InlineKeyboardBuilder()
        if user.gender == "M":
            builder.add(InlineKeyboardButton(text="📝 Записаться на уведомление", callback_data="awaiting_brother"))
            await msg.answer(brother_text, parse_mode="Markdown", reply_markup=builder.as_markup())
        elif user.gender == "F":
            builder.add(InlineKeyboardButton(text="Записаться", url="https://t.me/aysha_5663"))
            await msg.answer(sister_text, parse_mode="Markdown", reply_markup=builder.as_markup())
        else:
            text2 = (
                "📚 *Если вы хотите обучаться в группе с опытным Устазом или Устазой, "
                "мы подготовили удобный формат обучения онлайн.*\n\n"
                "👥 В группе вы сможете:\n"
                "• Получать обратную связь от преподавателя в реальном времени\n"
                "• Совместно практиковать чтение Корана\n"
                "• Усваивать правила Таджвида быстрее благодаря групповому взаимодействию\n\n"
                "✨ *Чтобы мы могли подобрать подходящую группу, укажите, пожалуйста, ваш пол:*"
            )
            builder.add(InlineKeyboardButton(text="🤵‍♂️ Я Брат", callback_data="im_brother"))
            builder.add(InlineKeyboardButton(text="🧕 Я Сестра", callback_data="im_sister"))
            builder.adjust(2)
            await msg.answer(text2, reply_markup=builder.as_markup(), parse_mode="Markdown")
    # if created:
    #     builder = InlineKeyboardBuilder()
    #     builder.add(InlineKeyboardButton(text="Я Брат", callback_data="new_user_brother"))
    #     builder.add(InlineKeyboardButton(text="Я Сестра", callback_data="new_user_sister"))
    #     builder.adjust(2)
    #     text = "Салям Алейкум, давай знакомится"
    #     await msg.answer(text, reply_markup=builder.as_markup())

@router.callback_query(F.data == "awaiting_brother")
async def awaiting_brother(call: CallbackQuery):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=call.from_user.id)
    wait, created = await sync_to_async(Wait.objects.get_or_create)(user=user)
    await call.answer("Ожидайте уведомлении о занятиях", show_alert=True)

@router.message(Command("brothers"))
async def brothers(msg: Message, bot: Bot):
    brothers = await sync_to_async(Wait.objects.all)()
    text = ""
    count = 0
    for brother in brothers:
        text += f"{brother.user.first_name} {brother.user.last_name}\n"
        count += 1
    await msg.answer(f"{count}")
    await msg.answer(text)

@router.message(Command("sisters"))
async def sisters(msg: Message, bot: Bot):
    sisters = await sync_to_async(TelegramUser.objects.filter)(gender="F")
    text = ""
    count = 0
    if sisters:
        for sister in sisters:
            text += f"{sister.first_name} {sister.last_name}\n"
            count += 1
        await msg.answer(f"{count}")
        await msg.answer(text)

@router.chat_join_request()
async def chat_join_request(event: ChatJoinRequest):
    user_id = event.from_user.id
    try:
        # user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=user_id)
        # user.username = event.from_user.username
        # user.first_name = event.from_user.first_name
        # user.last_name = event.from_user.last_name
        # user.save()

        full_name = event.from_user.full_name
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Забрать материал", url="https://t.me/An_Nur_robot?start=material"))
        text = (
            f"🌙 Ассаляму алейкум, *{full_name}*! \n\n"
            "Да вознаградит вас Аллах за ваши намерения научиться читать Коран и пусть Аллах облегчит вам обучение. Аминь! 🤲\n\n"
            "📖 От Усмана (да будет доволен им Аллах) передаётся, что Пророк ﷺ сказал:\n"
            "*«Лучший из вас — тот, кто обучается Корану и обучает ему других»*\n\n"
            "_[Достоверный] - [Передал аль-Бухари] - [صحيح البخاري - 5027]_"
        )
        await event.bot.send_message(
            chat_id=user_id,
            text=text, reply_markup=builder.as_markup(), parse_mode="Markdown")
    except Exception:
        print(f"⚠️ Не удалось написать пользователю {user_id} — он не начал чат с ботом.")

    await event.approve()

@router.callback_query(F.data == "im_brother")
async def im_brother(call: CallbackQuery):
    await call.message.delete()
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=call.from_user.id)
    user.username = call.from_user.username
    user.first_name = call.from_user.first_name
    user.last_name = call.from_user.last_name
    user.gender = "M"
    await sync_to_async(user.save)()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="📝 Записаться на уведомление", callback_data="awaiting_brother"))
    await call.message.answer(brother_text, parse_mode="Markdown", reply_markup=builder.as_markup())

@router.callback_query(F.data == "im_sister")
async def im_siser(call: CallbackQuery):
    user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=call.from_user.id)
    user.username = call.from_user.username
    user.first_name = call.from_user.first_name
    user.last_name = call.from_user.last_name
    user.gender = "F"
    user.save()
    await call.message.delete()
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="Записаться", url="https://t.me/aysha_5663"))
    await call.message.answer(sister_text, parse_mode="Markdown", reply_markup=builder.as_markup())

class PostState(StatesGroup):
    awaiting_text = State()

class SendToSistersState(StatesGroup):
    awaiting_text = State()

@router.message(Command("send_sisters"))
async def sisters(msg: Message, state: FSMContext, bot: Bot):
    await msg.answer("Ваш текст:")
    await state.set_state(SendToSistersState.awaiting_text)

@router.message(SendToSistersState.awaiting_text)
async def send_to_sisters(msg: Message, bot: Bot, state: FSMContext):
    sisters = await sync_to_async(TelegramUser.objects.filter)(gender="F")
    good = 0
    fault = 0
    for sister in sisters:
        try:
            await bot.send_message(chat_id=sister.user_id, text=msg.text)
            good += 1
        except Exception as e:
            fault += 1
            print(e)
    await msg.answer(f"Отправлено {good} сёстрам\nОшибка при отправлении {fault} сёстрам")
    await state.clear()


@router.message(Command("post"))
async def new_post(msg: Message, state: FSMContext):
    # user = await sync_to_async(TelegramUser.objects.get)(user_id=msg.from_user.id)
    # if user.admin:
    await msg.answer("Введите текст:")
    await state.set_state(PostState.awaiting_text)

@router.message(PostState.awaiting_text)
async def post_awaiting_text(msg: Message, state: FSMContext, bot: Bot):
    user_id = "@An_Nur_Official"
    try:
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="☀️ 𝗔𝗡-𝗡𝗨𝗥 🌙 [хᴀдиᴄы, ᴀяᴛы]", url="https://t.me/+f9fH25BXvLYwMDFi"))
        copy = await bot.copy_message(chat_id=user_id, from_chat_id=msg.chat.id, message_id=msg.message_id, reply_markup=builder.as_markup())
        await bot.send_message(
            chat_id=user_id,
            text=msg.text)
        await state.clear()
    except Exception as e:
        print(e)


# @router.chat_member(ChatMemberUpdatedFilter(member_status_changed=IS_MEMBER))
# async def on_user_subscribe(event: ChatMemberUpdated, bot: Bot, state: FSMContext):
#     user = event.from_user
#
#     try:
#         await bot.send_message(user.id, f"Ассаляму алейкум, {user.first_name}! 🌙 Спасибо за подписку!")
#     except Exception as e:
#         print(f"⚠️ Не удалось отправить сообщение пользователю {user.id}: {e}")
