import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from bot.handlers.start_handler import start_handler
from bot.handlers.menu_handler import menu_handler
from bot.handlers.checkout_handler import checkout_handler

# Устанавливаем уровень логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Получаем токен бота из файла конфигурации
with open('config/token.txt', 'r') as file:
    token = file.read().strip()

def main():
    # Инициализация бота с помощью токена
    updater = Updater(token=token, use_context=True)
    dispatcher = updater.dispatcher

    # Регистрация обработчиков команд
    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('menu', menu_handler))
    dispatcher.add_handler(CommandHandler('checkout', checkout_handler))

    # Регистрация обработчика сообщений от пользователя
    dispatcher.add_handler(MessageHandler(Filters.text, handle_message))

    # Запуск бота
    updater.start_polling()
    updater.idle()

def handle_message(update, context):
    # Обработка сообщения от пользователя
    message = update.message.text
    # Ваша логика обработки сообщения
    # ...

if __name__ == '__main__':
    main()
