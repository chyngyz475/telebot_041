from aiogram.dispatcher.filters.state import StatesGroup, State


class MenuState(StatesGroup):
    MainMenu = State()  # Главное меню
    Checkout = State()  # Оформление заказа
    Calculator = State()  # Калькулятор
    Answers = State()  # Ответы на популярные вопросы
    Contact = State()  # Связь с менеджером
    OrderStatus = State()  # Статус заказа
    Course = State()  # Курс
    Delivery = State()  # Доставка
    # Добавьте здесь другие состояния, связанные с меню

