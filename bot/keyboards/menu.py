from aiogram import types
from aiogram import Router

router = Router()
# Inline keyboard buttons
menu_buttons = {
    'checkout': '🛒 Оформление заказа',
    'calculator': '🧮 Калькулятор',
    'answers': '❓ Ответы на популярные вопросы',
    'contact': '📞 Связь с менеджером',
    'status': '📦 Статус заказа',
    'course': '🎓 Курс',
    'delivery': '🚚 Доставка',
    'order_history': '📜 История заказов'
}
