import json

from aiogram import Router, F, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from database import db
from utils import messages
from keyboards.url_kb import get_url_keyboard

router = Router()


class PayVerify(StatesGroup):
    user_fetch_all = State()
    user_get_and_delete = State()
    user_notify = State()


@router.message(Command(commands=['verify']))
async def user_fetch_all(message: Message, state: FSMContext):
    await message.answer("Pass pls:")
    await state.set_state(PayVerify.user_fetch_all)


@router.message(PayVerify.user_fetch_all, F.text)
async def admin_password(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    if message.text == '12345':
        users = await db.get_all_from_db()
        users_list = ''
        for user in users:
            users_list += f'id: {user[0]}; email: {user[1]}; password: {user[2]};\n'
        await message.answer(users_list)
        await message.answer(messages.Messages.user_get_one)
        await state.set_state(PayVerify.user_get_and_delete)
    else:
        await state.clear()


@router.message(PayVerify.user_get_and_delete, F.text)
async def user_email_verify(message: Message, state: FSMContext):
    user_id = message.text
    user = await db.get_one_from_db(user_id)
    user_data = {'email': user[1], 'password': user[2]}
    user_json = json.dumps(user_data)
    # TODO: Отправка на сервер для регистрации на платформе
    await db.delete_from_db(user_id)
    await message.answer(messages.Messages.user_chat_id)
    await state.set_state(PayVerify.user_notify)


@router.message(PayVerify.user_notify, F.text)
async def user_notify(message: Message, state: FSMContext, bot: Bot):
    user_chat_id = message.text
    button_url = get_url_keyboard()
    await bot.send_message(user_chat_id, messages.Messages.user_success_message, reply_markup=button_url.as_markup())
    await state.clear()
