from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config_reader import config
from database import db
from utils import messages

router = Router()


class UserRegister(StatesGroup):
    user_email = State()
    user_password = State()
    user_payed = State()


@router.message(Text(text=messages.Messages.register_btn, ignore_case=True))
async def user_register_email(message: Message, state: FSMContext):
    await message.answer(messages.Messages.email_req, reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserRegister.user_email)


@router.message(UserRegister.user_email, F.text)
async def user_register_password(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer(messages.Messages.password_req)
    await state.set_state(UserRegister.user_password)


@router.message(UserRegister.user_password, F.text)
async def user_register_confirm(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(password=message.text)
    await message.answer(messages.Messages.payed_req)
    await state.set_state(UserRegister.user_payed)


@router.message(UserRegister.user_payed, F.photo)
async def user_register_photo(message: Message, state: FSMContext, bot: Bot):
    user_data = await state.get_data()
    await bot.send_message(config.admin_id, f'Пользователь: {user_data} Chat_id: {message.chat.id}')
    await db.add_to_db(user_data)
    photo = message.photo[-1].file_id
    await bot.send_photo(chat_id=config.admin_id, photo=photo)
    await message.answer(messages.Messages.payed_verify)
    await state.clear()
