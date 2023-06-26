from telegram import KeyboardButton, ReplyKeyboardMarkup

def get_back_keyboard():
    back_button = KeyboardButton('Назад')
    back_keyboard = ReplyKeyboardMarkup([[back_button]], resize_keyboard=True)
    return back_keyboard
