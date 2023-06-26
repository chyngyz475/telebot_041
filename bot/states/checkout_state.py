from aiogram.dispatcher.filters.state import StatesGroup, State


class CheckoutState(StatesGroup):
    Name = State()  # Ввод имени
    SKU = State()  # Ввод артикула
    Color = State()  # Ввод цвета товара
    Size = State()  # Ввод размера
    Amount = State()  # Ввод суммы
    Photo = State()  # Загрузка фото оплаты
    # Добавьте здесь другие состояния, связанные с оформлением заказа

