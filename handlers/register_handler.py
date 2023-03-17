from aiogram import Router, F, Bot
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove

from config_reader import config
from keyboards.payed_kb import get_payed_kb

router = Router()


class UserRegister(StatesGroup):
    user_email = State()
    user_password = State()


@router.message(Text(text="зарегистрироваться", ignore_case=True))
async def user_register_email(message: Message, state: FSMContext):
    await message.answer("Введите ваш email:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(UserRegister.user_email)

@router.message(UserRegister.user_email, F.text)
async def user_register_password(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await message.answer("Спасибо. Теперь нужно ввести пароль:")
    await state.set_state(UserRegister.user_password)

@router.message(UserRegister.user_password, F.text)
async def user_register_confirm(message: Message, state: FSMContext, bot: Bot):
    await state.update_data(password=message.text)
    user_data = await state.get_data()
    await message.answer(f'Прекрасно! {message.from_user.username} Остался последний шаг. Для доступа к урокам необходимо оплатить курс. Для этого нажмите кнопку оплатить', reply_markup=get_payed_kb())
    await bot.send_message(config.admin_id, f'Пользователь: {user_data} зарегистрировался!')
    await state.clear()
    