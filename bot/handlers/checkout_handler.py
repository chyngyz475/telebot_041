import psycopg2
from telegram import Update, Bot
from telegram.ext import CallbackContext
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from states.base_state import CalculatorState, StatusForm


dp = Dispatcher()
# Калькулятор расчет стоимости заказа

@dp.callback_query_handler(lambda query: query.data == 'calculator')
async def handle_calculator(query: types.CallbackQuery):
    await query.message.reply("Расчет стоимости товара\n\nПожалуйста, введите цену:")

    # Ввод цен
    await CalculatorState.price.set()

@dp.message_handler(state=CalculatorState.price)
async def process_price(message: types.Message, state: FSMContext):
    try:
        price = float(message.text)
    except ValueError:
        await message.reply("Неверный формат цены. Пожалуйста, введите действительную цену.")
        return

    # добавление суммы валюты и курса
    exchange_rate = 11.5  # Примерные значение
    commission = 8  # Примерные значение

    total_cost = price * exchange_rate + commission

    await message.reply(f"Цена: {price}\nКурс юаня: {exchange_rate}\nКоммиссия: {commission}\nОбщая стоимость: {total_cost} рублей \n")

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)
    await state.finish()

# Калькулятор расчет стоимости заказа

# Контакты
@dp.callback_query_handler(lambda query: query.data == 'contact')
async def handle_contact_manager(query: types.CallbackQuery):
    message_text = "Связь менеджером\n\n"
    message_text += "Убедительная просьба, не писать менеджеру по вопросам, которые есть в разделе «ответы на популярные вопросы». \n"
    message_text += " Пожалуйста, повторно прочтите  информацию и может быть вы найдете ответ на свой вопрос.\n"
    message_text += "Менеджеру стоит писать в том случае, если у вас возникли вопросы после оформления заказа. \n\n"
    message_text += "Вы можете связаться с нами в Telegram.\n"
    message_text += "Аккаунт нашего менеджера : @admin021\n\n"

    keyboard = types.InlineKeyboardMarkup()
    button = types.InlineKeyboardButton("Open Telegram", url="https://t.me/chyngyz0411")
    keyboard.add(button)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)

    await query.message.reply(message_text, reply_markup=keyboard)
# Контакты



# доставка
@dp.callback_query_handler(lambda query: query.data == 'delivery')
async def handle_delivery(query: types.CallbackQuery):
    delivery_info = [
        "Доставка оплачивается по факту в Москве, перед получением. Когда заказ приходит к нам, мы взвешиваем его и рассчитываем стоимость",
        " 🚗 Авто доставка 890 рублей за кг (15-25 дня)",
        "✈️ Авиа доставка 1190 рублей за кг (12-15 дней)",
        "(Сроки с учетом того, что площадка отправила нам заказ без задержек)",
        "Расчет доставки производится без округления веса.Если посылка, например, 1,3кг значит, стоимость доставки*1.3   "
    ]

    message_text = "\n".join(delivery_info)

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)

    await query.message.reply(message_text, parse_mode='HTML', reply_markup=keyboard)

# доставка





# Статус заказа



@dp.callback_query_handler(lambda query: query.data == 'status', state=None)
async def ask_for_product_id(query: types.CallbackQuery):
    await StatusForm.ID_PRODUCT.set()
    await query.message.reply("Введите ID товара:")

@dp.message_handler(state=StatusForm.ID_PRODUCT)
async def process_product_id(message: types.Message, state: FSMContext):
    product_id = message.text

    cursor = conn.cursor()
    conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='telebot',
            user='telebot',
            password='xsyusp'
        )
    try:
        cursor.execute("SELECT * FROM telegram_wholesaleordertelegtam WHERE unique_id = %s", (product_id,))
        wholesale_order = cursor.fetchone()

        if wholesale_order:
            expected_status = wholesale_order[5]
            status_mapping = {
                1: 'Доставлено',
                2: 'Статус актуально',

            }
            expected_status_text = status_mapping.get(expected_status, 'Неизвестный статус')

            message_text = f"Статус товара ID: {product_id}\nОжидаемый статус заказа: {expected_status_text}"
        else:
            message_text = f"Заказ с ID {product_id} не найден"
    except Exception as e:
        message_text = f"Произошла ошибка: {str(e)}"

    cursor.close()

    await message.reply(message_text)



# Статус заказа



# Курс валют
@dp.callback_query_handler(lambda query: query.data == 'course')
async def handle_course(query: types.CallbackQuery):
    exchange_rate = 11.5  # Заменить фактическим обменным курсом

    message_text += f"Текущий курс на сегодняшний день 12.4\n"

    
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("❓ Ответы на популярные вопросы", callback_data='answers'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)

    await query.message.reply(message_text, reply_markup=keyboard)

# Курс валют




# Ответы на популярные вопросы

@dp.callback_query_handler(lambda query: query.data == 'answers')
async def handle_answers(query: types.CallbackQuery):
    # Получите ответы на популярные вопросы из вашего источника данных или базы данных
    

    message_text = "Ответы на часто задаваемые вопросы вы можете найти в нашем FAQ\n\n"
    message_text += "📚 Если у вас появятся вопросы, вы можете найти ответы в нашем разделе справки.\n\n"
    message_text += "🔗 Перейдите по ссылке для получения дополнительной информации.\n\n"


    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Open Telegram", url="https://telegra.ph/FAQ-06-16-9#%D0%9A%D0%B0%D0%BA-%D0%BF%D1%80%D0%B0%D0%B2%D0%B8%D0%BB%D1%8C%D0%BD%D0%BE-%D0%BE%D1%84%D0%BE%D1%80%D0%BC%D0%BB%D1%8F%D1%82%D1%8C-%D0%B7%D0%B0%D0%BA%D0%B0%D0%B7 "),
        types.InlineKeyboardButton("Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)
    await query.message.reply(message_text, parse_mode='HTML', reply_markup=keyboard)

# Ответы на популярные вопросы

    # ...
