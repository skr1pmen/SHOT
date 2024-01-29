from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from config import ADMIN
from functions.commands import Commands
from functions.utils import Utils
from aiogram.fsm.context import FSMContext
from keyboards.admin_kb import admin_kb

router = Router()
cmd = Commands()


@router.message(CommandStart())
async def command_start_handler(message: Message, state: FSMContext):
    if message.chat.type == "private":
        if message.from_user.id in ADMIN:
            await message.answer("Привет", reply_markup=admin_kb)
    elif "group" in message.chat.type:
        if not cmd.group_exists(message.chat.id):
            await message.answer("Теперь эта группа будет получать расылку")
            cmd.add_group(message)


@router.message()
async def echo_handler(message: Message):
    await message.answer(message.text)