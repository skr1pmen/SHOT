import asyncio
import tracemalloc

from aiogram import Bot, Dispatcher
from config import *
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram.filters import CommandStart
from aiogram.types import Message
from database import base
from datetime import datetime
import tracemalloc

tracemalloc.start()


class Commands:
    def __init__(self):
        self.db = base.Database(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )

    def group_exists(self, chat_id):
        response = self.db.fetch(f"SELECT COUNT(*) FROM groups WHERE chat_id = {chat_id}")[0][0]
        return bool(response)

    def add_group(self, msg):
        self.db.execute(f"INSERT INTO groups (chat_id, name) VALUES ({msg.chat.id}, '{msg.chat.title}')")

    async def get_message(self):
        response = self.db.fetch(f"SELECT chat_id, days_of_week, message FROM groups")
        day = datetime.weekday(datetime.now())
        for group in response:
            chat_id = group[0]
            days = group[1]
            message = group[2]
            if str(day) in days:
                try:
                    await get_message_cmd(chat_id, message)
                except:
                    continue


bot = Bot(TOKEN, parse_mode="HTML")
dp = Dispatcher()
cmd = Commands()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    if message.chat.type == "private":
        if message.from_user.id in ADMIN:
            await message.answer("Привет")
    elif "group" in message.chat.type:
        if not cmd.group_exists(message.chat.id):
            await message.answer("Теперь эта группа будет получать раcсылку")
            cmd.add_group(message)


@dp.message()
async def get_message_cmd(chat_id, message):
    await bot.send_message(int(chat_id), message)


@dp.message()
async def echo_handler(message: Message):
    await message.answer(message.text)


async def main():
    print("Bot started")
    scheduler = AsyncIOScheduler(timezone="Europe/Astrakhan")
    scheduler.add_job(cmd.get_message, "cron", day="*", hour="10", minute="00")
    scheduler.start()
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot dead")
