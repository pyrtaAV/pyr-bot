import asyncio
from aiogram import Bot, Dispatcher
import logging

from config_reader import config
from handlers import common, register_handler, admin_verify
from database import db


async def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(name)s - %(message)s")
    bot = Bot(token=config.bot_token.get_secret_value(), parse_mode="HTML")
    dp = Dispatcher()
    db.sql_start()

    dp.include_router(common.router)
    dp.include_router(register_handler.router)
    dp.include_router(admin_verify.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    db.sql_stop()


if __name__ == "__main__":
    asyncio.run(main())
