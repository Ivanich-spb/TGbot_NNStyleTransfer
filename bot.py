import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from os import getenv
from sys import exit
from app.handlers import register_handlers

bot_token = getenv("BOT_TOKEN")
if not bot_token:
    exit("Error: no token provided")

# Объект бота
bot = Bot(token=bot_token)
# Диспетчер для бота
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO
                    )

register_handlers(dp)

if __name__ == "__main__":
    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
