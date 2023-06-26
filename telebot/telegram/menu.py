from aiogram import types


# Inline keyboard buttons
menu_buttons = {
    'checkout': 'Оформление заказа',
    'calculator': 'Калькулятор',
    'answers': 'Ответы на популярные вопросы',
    'contact': 'Связь с менеджером',
    'status': 'Статус заказа',
    'course': 'Курс',
    'delivery': 'Доставка'
}


def get_menu_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(text=value, callback_data=key) for key, value in menu_buttons.items()]
    keyboard.add(*buttons)
    return keyboard


def get_back_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back_button = types.InlineKeyboardButton(text='Back', callback_data='back')
    keyboard.add(back_button)
    return keyboard

def get_checkout_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    retail_button = types.InlineKeyboardButton(text='Розничный', callback_data='checkout_retail')
    wholesale_button = types.InlineKeyboardButton(text='Оптовая', callback_data='checkout_wholesale')
    keyboard.add(retail_button, wholesale_button)
    return keyboard

