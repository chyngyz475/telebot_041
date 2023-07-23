import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from menu import get_menu_keyboard, get_back_keyboard, get_checkout_keyboard
from menu import menu_buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from openpyxl import Workbook
import psycopg2
import uuid
from aiogram.dispatcher.filters.state import State, StatesGroup
from datetime import datetime




def generate_item_id():
    # Generate a unique item ID using UUID (Universally Unique Identifier)
    item_id = str(uuid.uuid4())
    return item_id

workbook = Workbook()
sheet = workbook.active

status_id = 1

conn = psycopg2.connect(
    host='localhost',
    port='5432',
    database='telebot',
    user='telebot',
    password='xsyusp'
)

class CalculatorState(StatesGroup):
    price = State()

    price = State()

class CheckoutRetailState(StatesGroup):
    name = State()    
    sku = State()    
    color = State()   
    size = State()    
    amount = State()  
    photo = State()   

class CheckoutWholesaleState(StatesGroup):
    username = State()
    quantitywh = State()
    item_details = State()
    sizewh = State()
    amountwh = State()
    photo = State() 
  

class StatusForm(StatesGroup):
    ID_PRODUCT = State()


API_TOKEN = '6264165442:AAEQsZpC61iYI49cCl8iEjFlBlRnaQw0kr4' 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Здравствуйте, добро пожаловать в бот группы "Хороший бизнес" ! Мы рады, что выбрали нас. ', reply_markup=get_menu_keyboard())


@dp.message_handler(commands=['help'])
async def help_handler(message: types.Message):
    await message.reply('если у вас есть вопросы', reply_markup=get_menu_keyboard())


@dp.message_handler(commands=['menu'])
async def menu_handler(message: types.Message):
    await message.reply('Меню главное', reply_markup=get_menu_keyboard())




@dp.callback_query_handler(lambda query: query.data == 'back', state='*')
async def process_back_callback(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)
    await query.message.edit_text('Main Menu', reply_markup=get_menu_keyboard())
    await state.finish()  # Очистить текущее состояние


# Оформить заказ
@dp.callback_query_handler(lambda query: query.data == 'checkout')
async def handle_checkout(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)

    await query.message.reply("Пожалуйста, выберите вариант:", reply_markup=keyboard)


# Оформить заказ


# Розничная торговля

@dp.callback_query_handler(lambda query: query.data == 'checkout_retail')
async def handle_checkout_retail(query: types.CallbackQuery):
    await CheckoutRetailState.first()
    await query.message.reply("Введите свое имя пользователя в телеграмм через @, чтобы создать заказ:")


@dp.message_handler(state=CheckoutRetailState.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()

    await state.update_data(name=name)
    await CheckoutRetailState.next()
    await message.reply("Введите артикул C POIZON:")


@dp.message_handler(state=CheckoutRetailState.sku)
async def process_sku(message: types.Message, state: FSMContext):
    sku = message.text.strip()

    await state.update_data(sku=sku)
    await CheckoutRetailState.next()
    await message.reply("Введите цвет товара:")


@dp.message_handler(state=CheckoutRetailState.color)
async def process_color(message: types.Message, state: FSMContext):
    color = message.text.strip()

    await state.update_data(color=color)
    await CheckoutRetailState.next()
    await message.reply("Введите размер:")


@dp.message_handler(state=CheckoutRetailState.size)
async def process_size(message: types.Message, state: FSMContext):
    size = message.text.strip()

    await state.update_data(size=size)
    await CheckoutRetailState.next()
    await message.reply("Введите сумму:")


@dp.message_handler(state=CheckoutRetailState.amount)
async def process_amount(message: types.Message, state: FSMContext):
    amount_in_yuan = message.text.strip()

    exchange_rate = 9.6  
    amount_in_rubles = float(amount_in_yuan) * exchange_rate

    await state.update_data(amount=amount_in_yuan)
    await CheckoutRetailState.next()

    data = await state.get_data()
    name = data['name']
    sku = data['sku']
    color = data['color']
    size = data['size']
    amount_in_yuan = data['amount']
    amount_in_rubles = amount_in_rubles

    creation_date = datetime.now()

    item_id = generate_item_id() 

    message_text = "📦 Подтверждение заказа:\n\n"
    message_text += f"👤 Full Name: {name}\n"
    message_text += f"🆔 Product ID: {item_id}\n"
    message_text += f"🏷️ Product SKU: {sku}\n"
    message_text += f"🎨 Color: {color}\n"
    message_text += f"📏 Size: {size}\n"
    message_text += f"💰 Amount in Yuan: {amount_in_yuan} CNY\n"
    message_text += f"💵 Amount in Rubles: {amount_in_rubles:.2f} RUB\n\n"
    message_text += "💳 Оплата производится переводом на карту.\n\n"
    message_text += "✅ Рабочие карта ✅\n"
    message_text += "🏦 Тинькофф Номер карты Получатель\n"
    message_text += "2211220088889991\n"
    message_text += "👤 Иванов Иван Иванович\n\n"
    message_text += "📷 После оплаты присылайте чек/фото перевода.\n"
    message_text += "✉️ Отправьте скриншот оплаты.\n"

    await message.reply(message_text)
    await CheckoutRetailState.photo.set()

       
    order = {
        'item_id': item_id,
        'name': name,
        'sku': sku,
        'color': color,
        'size': size,
        'amount_in_yuan': amount_in_yuan,
        'amount_in_rubles': amount_in_rubles,
        'creation_date': creation_date
    }
    order_history.append(order)

    
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telegram_application (name, sku, color, size, amount, status_id, creation_date ) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, sku, color, size, amount_in_yuan, amount_in_rubles, status_id, creation_date)
    )
    conn.commit()

  
    row = [name, sku, color, size, amount_in_yuan, amount_in_rubles,]
    sheet.append(row)
    workbook.save('orders.xlsx')


@dp.message_handler(content_types=types.ContentType.PHOTO, state=CheckoutRetailState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    data = await state.get_data()
    name = data['name']
    sku = data['sku']
    color = data['color']
    size = data['size']
    amount = data['amount']

    await message.reply("Заказ успешно размещен. Спасибо, мы скоро свяжемся с вами!", reply_markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    types.KeyboardButton("Меню")
))

    # Сбросить состояние, чтобы начать новый заказ
    await state.reset_state()


#история заказов 

order_history = []  # Определяем список истории заказов

@dp.callback_query_handler(lambda query: query.data == 'order_history')
async def handle_order_history(query: types.CallbackQuery):
    # Получить историю заказов
    order_history = handle_order_history()

    if order_history:
        message_text = "📜 Ваша история заказов:\n\n"
        for order in order_history:
            message_text += f"📦 Заказ ID: {order['item_id']}\n"
            message_text += f"📅 Дата создания: {order['creation_date']}\n"
            message_text += f"👤 Full Name: {order['name']}\n"
            message_text += f"🏷️ Product SKU: {order['sku']}\n"
            message_text += f"🎨 Color: {order['color']}\n"
            message_text += f"📏 Size: {order['size']}\n"
            message_text += f"💰 Amount in Yuan: {order['amount_in_yuan']} CNY\n"
            message_text += f"💵 Amount in Rubles: {order['amount_in_rubles']:.2f} RUB\n\n"
            message_text += "==============================\n\n"

        await query.message.reply(message_text)
    else:
        await query.message.reply("У вас пока нет заказов.")





# Оптовая торговля
@dp.callback_query_handler(lambda query: query.data == 'checkout_wholesale')
async def handle_checkout_wholesale(query: types.CallbackQuery):
    await CheckoutWholesaleState.username.set()
    await query.message.reply("Введите свое имя пользователя в телеграмм через @, чтобы создать заказ:")

@dp.message_handler(state=CheckoutWholesaleState.username)
async def process_username(message: types.Message, state: FSMContext):
    username = message.text.strip()

    await state.update_data(username=username)
    await CheckoutWholesaleState.next()
    await message.reply("Введите количество позиций в вашем заказе:")

@dp.message_handler(state=CheckoutWholesaleState.quantitywh)
async def process_quantity(message: types.Message, state: FSMContext):
    quantitywh = message.text.strip()

    await state.update_data(quantitywh=quantitywh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите артикул C POIZON и цвет кнопки для каждого товара, разделяя их по строкам. Например:\n"
                        "DD1903-100 Синяя\n"
                        "CW2288-111 Черная")

@dp.message_handler(state=CheckoutWholesaleState.item_details)
async def process_item_details(message: types.Message, state: FSMContext):
   # Разделите текст сообщения по строкам, чтобы получить несколько элементов в столбце
    items = message.text.strip().split('\n')

  # Проверяем, есть ли уже список для items_data в состоянии
    data = await state.get_data()
    items_data = data.get('items_data', [])

# Перебирать элементы и обрабатывать каждый артикул и цвет
    for item in items:
        item_details = item.split()
        if len(item_details) >= 2:
            skuwh = item_details[0]
            colorwh = ' '.join(item_details[1:])
            items_data.append((skuwh, colorwh))

   # Сохраняем обновленные items_data в состоянии
    await state.update_data(items_data=items_data)

    # Спросите размер каждого предмета
    await CheckoutWholesaleState.next()
    await message.reply("Введите размеры для каждого товара, разделяя их по строкам. Например:\n"
                        "M\n"
                        "L")

@dp.message_handler(state=CheckoutWholesaleState.sizewh)
async def process_size(message: types.Message, state: FSMContext):
    sizewh = message.text.strip()

    await state.update_data(sizewh=sizewh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите общую сумму заказа:")

@dp.message_handler(state=CheckoutWholesaleState.amountwh)
async def process_amount(message: types.Message, state: FSMContext):
    amountwh = message.text.strip()

    await state.update_data(amountwh=amountwh)
    await CheckoutWholesaleState.next()

    data = await state.get_data()
    username = data['username']
    quantitywh = data['quantitywh']
    items_data = data['items_data']
    sizewh = data['sizewh']
    amountwh = data['amountwh']

    message_text = f"👤 Пользователь: {username}\n"
    message_text += f"🛍️ Количество позиций: {quantitywh}\n"
    message_text += "📋 Детали заказа:\n"

# Перебираем элементы items_data и добавляем детали каждого элемента в message_text
    for i, (sku, color) in enumerate(items_data, start=1):
        message_text += f"Товар {i}:\n"
        message_text += f"  🏷️ Артикул C POIZON: {sku}\n"
        message_text += f"  🎨 Цвет кнопки: {color}\n"
        message_text += f"  📏 Размер: {sizewh}\n\n"

    message_text += f"💰 Общая сумма заказа: {amountwh}\n"
    message_text += "💳 Оплата производится переводом на карту.\n"
    message_text += "✅ Рабочие карта ✅\n"
    message_text += "🏦 Тинькофф Номер карты Получатель\n"
    message_text += "2211220088889991\n"
    message_text += "👤 Иванов Иван Иванович\n\n"
    message_text += "📷 После оплаты присылайте чек/фото перевода.\n"
    message_text += "✉️ Отправьте скриншот оплаты.\n"

    await message.reply(message_text)
    await CheckoutWholesaleState.photo.set()
    await message.reply("Пожалуйста, отправьте фото в качестве подтверждения оплаты.")

@dp.message_handler(content_types=types.ContentType.PHOTO, state=CheckoutWholesaleState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

# Сохраняем photo_id в базу данных или выполняем другие действия по мере необходимости
     # Замените этот код своей логикой интеграции с базой данных

    await message.reply("Заказ успешно размещен. Спасибо, мы скоро свяжемся с вами!")

    # Reset the state to start a new order
    await state.reset_state()

# Калькулятор расчет стоимости заказа

@dp.callback_query_handler(lambda query: query.data == 'calculator')
async def handle_calculator(query: types.CallbackQuery):
    await query.message.reply("Калькулятор - Расчет стоимости товара\n\nПожалуйста, введите цену:")

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
    commission = 0.8  # Примерные значение

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
        "Информация о доставке:",
        "Оплата за доставку производится сразу по приезде товара на склад, вне зависимости от колличества заказанных позиций. Когда заказ приходит к нам, мы взвешиваем его и рассчитываем стоимость.",
        " Авто доставка 750 рублей за кг (20-30 дней)",
        "Авиа доставка 950 рублей за кг (12-15 дней)",
        " (Сроки с учетом того, что площадка отправила нам заказ без задержек)Расчет доставки производится без округления веса.Если посылка, например, 1,3кг значит, стоимость доставки*1.4   "
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
@dp.message_handler(state=StatusForm.ID_PRODUCT)
async def process_product_id(message: types.Message, state: FSMContext):
    product_id = message.text

    try:
        order = Application.objects.get(product_id=product_id)
        expected_status = order.status  # Assuming `status` field is a CharField or similar
        status_mapping = {
            'pending': 'В ожидании',
            'processing': 'В обработке',
            'shipped': 'Отправлен',
            'delivered': 'Доставлен',
        }
        expected_status_text = status_mapping.get(expected_status, 'Неизвестный статус')

        message_text = f"Статус товара ID: {product_id}\nОжидаемый статус заказа: {expected_status_text}"
    except Application.DoesNotExist:
        message_text = f"Заказ с ID {product_id} не найден"

    await message.reply(message_text)

# Статус заказа



# Курс валют
@dp.callback_query_handler(lambda query: query.data == 'course')
async def handle_course(query: types.CallbackQuery):
    exchange_rate = 11.5  # Заменить фактическим обменным курсом

    message_text = f"Обменный курс:\n\n"
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
    

    message_text = "Ответы на популярные вопросы:\n\n"
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




if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
