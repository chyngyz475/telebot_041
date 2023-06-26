from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from handlers.start_handler import start_handler
from handlers.menu_handler import menu_handler
from handlers.checkout_handler import checkout_handler

TOKEN = '6264165442:AAEQsZpC61iYI49cCl8iEjFlBlRnaQw0kr4'

bot = Bot(token=TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Register handlers
dp.register_message_handler(start_handler, commands="start")
dp.register_message_handler(menu_handler, commands="menu")
dp.register_message_handler(checkout_handler, commands="checkout")

# Start polling
if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
