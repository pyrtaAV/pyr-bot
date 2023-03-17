from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.register_kb import get_register_kb

router = Router()


@router.message(Command(commands=["start"]))
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text=f"Добро пожаловать {message.from_user.username}. В первую очередь вам нужно зарегистрироваться",
        reply_markup=get_register_kb()
    )


@router.message(Command(commands=["cancel"]))
@router.message(Text(text="отмена"))
async def cmd_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        text="Действие отменено",
        reply_markup=ReplyKeyboardRemove()
    )