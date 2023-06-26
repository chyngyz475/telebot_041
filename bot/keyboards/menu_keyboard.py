from telegram import KeyboardButton, ReplyKeyboardMarkup

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
    buttons = [KeyboardButton(text) for text in menu_buttons.values()]
    menu_keyboard = ReplyKeyboardMarkup(build_menu(buttons, n_cols=2), resize_keyboard=True)
    return menu_keyboard

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu
