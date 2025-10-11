import os

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, CallbackQuery, \
    FSInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder
from asgiref.sync import sync_to_async
from aiogram.types import ChatJoinRequest

from tg.models import TelegramUser

router = Router()

# @router.message(Command("start"))
# async def start_command(msg: Message):
#     user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=msg.from_user.id)
#     user.username = msg.from_user.username
#     user.first_name = msg.from_user.first_name
#     user.last_name = msg.from_user.last_name
#     user.save()
#
#     if created:
#         builder = InlineKeyboardBuilder()
#         builder.add(InlineKeyboardButton(text="Я Брат", callback_data="new_user_brother"))
#         builder.add(InlineKeyboardButton(text="Я Сестра", callback_data="new_user_sister"))
#         builder.adjust(2)
#         text = "Салям Алейкум, давай знакомится"
#         await msg.answer(text, reply_markup=builder.as_markup())

@router.chat_join_request()
async def chat_join_request(event: ChatJoinRequest):
    try:
        user, created = await sync_to_async(TelegramUser.objects.get_or_create)(user_id=event.from_user.id)
        user.username = event.from_user.username
        user.first_name = event.from_user.first_name
        user.last_name = event.from_user.last_name
        user.save()
        user_id = event.from_user.id
        full_name = event.from_user.full_name
        builder = InlineKeyboardBuilder()
        builder.add(InlineKeyboardButton(text="Забрать материал", callback_data="give_me_material"))

        await event.bot.send_message(
            chat_id=user_id,
            text=f"Ассаляму алейкум, {full_name}! 🌙\n"
                 "Спасибо за интерес к нашему каналу.\n"
                 "Пожалуйста, нажмите /start у бота, чтобы завершить регистрацию.", reply_markup=builder.as_markup())
    except Exception:
        print(f"⚠️ Не удалось написать пользователю {user_id} — он не начал чат с ботом.")

    await event.approve()

@router.callback_query(F.data == "give_me_material")
async def give_me_material(call: CallbackQuery):

    base_dir = os.path.dirname(__file__)
    pdf_path = os.path.join(base_dir, "AZHARIA_arabic.pdf")
    pdf_file = FSInputFile(pdf_path, filename="AZHARIA_arabic.pdf")
    await call.message.answer_document(
        document=pdf_file,
    )
    await call.answer("")
