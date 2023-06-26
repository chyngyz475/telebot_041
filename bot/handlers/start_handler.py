from telegram import Update, Bot
from telegram.ext import CallbackContext

def start_handler(update: Update, context: CallbackContext):
    # Получаем объект бота из контекста
    bot: Bot = context.bot
    # Получаем объект чата из сообщения
    chat_id = update.message.chat_id

    # Отправляем приветственное сообщение пользователю
    bot.send_message(chat_id=chat_id, text="Привет! Я бот. Как могу помочь?")

    # Дополнительная логика обработки команды /start
    # ...
