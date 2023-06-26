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
    namewh = State()    
    skuwh = State()     
    colorwh = State()   
    sizewh = State()   
    amountwh = State()  
    photo = State()   

class StatusForm(StatesGroup):
    ID_PRODUCT = State()
    # Add more states if needed

API_TOKEN = '6264165442:AAEQsZpC61iYI49cCl8iEjFlBlRnaQw0kr4'  # Замените своим токеном Telegram Bot API

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
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Назад", callback_data='back')
    ]
    keyboard.add(*buttons)
    await query.message.edit_text('Main Menu', reply_markup=get_menu_keyboard())
    await state.finish()  # Очистить текущее состояние


# Оформить заказ
@dp.callback_query_handler(lambda query: query.data == 'checkout')
async def handle_checkout(query: types.CallbackQuery):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Назад", callback_data='back')
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
    amount = message.text.strip()

    await state.update_data(amount=amount)
    await CheckoutRetailState.next()

    data = await state.get_data()
    name = data['name']
    sku = data['sku']
    color = data['color']
    size = data['size']
    amount = data['amount']

    item_id = generate_item_id()  # Функция для генерации уникального идентификатора товара

    message_text = f"Подтверждение заказа:\n\n"
    message_text += f"Full Name: {name}\n"
    message_text += f"Product ID: {item_id}\n" 
    message_text += f"Product SKU: {sku}\n"
    message_text += f"Color: {color}\n"
    message_text += f"Size: {size}\n"
    message_text += f"Amount: {amount}\n\n"
    message_text += f"Оплата производится переводом на карту.\n"
    message_text += f"✅Рабочие карта✅\n"
    message_text += f"Тинькофф Номер карты Получатель\n"
    message_text += f"2211220088889991\n"
    message_text += f"Иванов Иван Иванович\n"
    message_text += "После оплаты присылайте чек/фото перевода.\n"
    message_text += f"Отправьте скриншот оплаты.\n"

    await message.reply(message_text)
    await CheckoutRetailState.photo.set()

    # Save the data in the PostgreSQL database
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO telegram_application (name, sku, color, size, amount, status_id) VALUES (%s, %s, %s, %s, %s, %s)",
        (name, sku, color, size, amount, status_id)
    )
    conn.commit()

    # Save the data in the Excel file
    row = [name, sku, color, size, amount]
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

    await message.reply("Заказ успешно размещен. Спасибо, мы скоро свяжемся с вами!")

    # Сбросить состояние, чтобы начать новый заказ
    await state.reset_state()




# Оптовая торговля
@dp.callback_query_handler(lambda query: query.data == 'checkout_wholesale')
async def handle_checkout_wholesale(query: types.CallbackQuery):
    await CheckoutWholesaleState.first()
    await query.message.reply("Введите свое имя пользователя в телеграмм через @, чтобы создать заказ:")


@dp.message_handler(state=CheckoutWholesaleState.namewh)
async def process_name(message: types.Message, state: FSMContext):
    namewh = message.text.strip()

    await state.update_data(namewh=namewh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите артикул C POIZON:")


@dp.message_handler(state=CheckoutWholesaleState.skuwh)
async def process_sku(message: types.Message, state: FSMContext):
    skuwh = message.text.strip()

    await state.update_data(skuwh=skuwh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите цвет товара:")


@dp.message_handler(state=CheckoutWholesaleState.colorwh)
async def process_color(message: types.Message, state: FSMContext):
    colorwh = message.text.strip()

    await state.update_data(colorwh=colorwh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите размер:")


@dp.message_handler(state=CheckoutWholesaleState.sizewh)
async def process_size(message: types.Message, state: FSMContext):
    sizewh = message.text.strip()

    await state.update_data(sizewh=sizewh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите сумму:")


@dp.message_handler(state=CheckoutWholesaleState.amountwh)
async def process_amount(message: types.Message, state: FSMContext):
    amountwh = message.text.strip()

    await state.update_data(amountwh=amountwh)
    await CheckoutWholesaleState.next()

    data = await state.get_data()
    namewh = data['name']
    skuwh = data['sku']
    colorwh = data['color']
    sizewh = data['size']
    amountwh = data['amount']

    message_text = f"Подтверждение заказа:\n\n"
    message_text += f"Full Name: {namewh}\n"
    message_text += f"Product SKU: {skuwh}\n"
    message_text += f"Color: {colorwh}\n"
    message_text += f"Size: {sizewh}\n"
    message_text += f"Amount: {amountwh}\n\n"
    message_text += f"Оплата производится переводом на карту.\n"
    message_text += f"✅Рабочие карта✅\n"
    message_text += f"Тинькофф Номер карты Получатель\n"
    message_text += f"2211220088889991\n"
    message_text += f"Иванов Иван Иванович\n"
    message_text += "После оплаты присылайте чек/фото перевода.\n"
    message_text += f"Отправьте скриншот оплаты.\n"



    await message.reply(message_text)
    await CheckoutWholesaleState.photo.set()

    # Send the collected data to a Telegram account
    message_text = f"New Order\n\n"
    message_text += f"Full Name: {namewh}\n"
    message_text += f"Product SKU: {skuwh}\n"
    message_text += f"Color: {colorwh}\n"
    message_text += f"Size: {sizewh}\n"
    message_text += f"Amount: {amountwh}\n"

    chat_id = '@Chyngyz0411'

    await bot.send_message(chat_id='chat_id', text=message_text)


@dp.message_handler(content_types=types.ContentType.PHOTO, state=CheckoutWholesaleState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    data = await state.get_data()
    namewh = data['name']
    skuwh = data['sku']
    colorwh = data['color']
    sizewh = data['size']
    amountwh = data['amount']


    # Save all the collected data and photo to the database
    # Replace this code with your database integration logic



    await message.reply("Заказ успешно размещен. Спасибо мы скоро свяжемся с вами!")

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
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Назад", callback_data='back')
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
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Назад", callback_data='back')
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
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Назад", callback_data='back')
    ]
    keyboard.add(*buttons)

    await query.message.reply(message_text, parse_mode='HTML', reply_markup=keyboard)

# доставка





# Статус заказа
@dp.callback_query_handler(lambda query: query.data == 'status')
async def handle_status(query: types.CallbackQuery):
    message_text = "Введите ID товара:"
    await query.message.reply(message_text)
    await StatusForm.ID_PRODUCT.set()


@dp.message_handler(state=StatusForm.ID_PRODUCT)
async def process_product_id(message: types.Message, state: FSMContext):
    product_id = message.text

    # Check if the product exists in the database
    if product_exists(product_id):
        # Product exists, get its status
        product_status = get_product_status(product_id)

        message_text = f"Статус товара ID: {product_id}\n"
        message_text += f"Статус: {product_status}\n"
        # Add other details as needed

        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
            types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
            types.InlineKeyboardButton("Ответы на популярные вопросы", callback_data='answers'),
            types.InlineKeyboardButton("Калькулятор", callback_data='calculator'),
            types.InlineKeyboardButton("Назад", callback_data='back'),
        ]
        keyboard.add(*buttons)

        await message.reply(message_text, reply_markup=keyboard)
    else:
        # Product does not exist, prompt the user to order the product
        message_text = "Товар отсутствует. Пожалуйста, оформите заказ."
        await message.reply(message_text)



def product_exists(product_id):
    # Implement your logic to check if the product exists in the database
    # You can query the `telegram_application` table and check if the product_id exists
    # Return True if the product exists, or False otherwise
    return False


def get_product_status(product_id):
    # Implement your logic to retrieve the status of the product from the database
    # You can query the `telegram_application` table and fetch the status based on the product_id
    # Return the status as a string
    return "Product not found"


async def handle_checkout(message: types.Message, state: FSMContext):
    # Implement the logic to handle the order checkout process
    # This may involve creating an order, collecting payment details, etc.
    # You can use the `state` to track the necessary data during the order checkout process
    # After completing the order checkout, you can return the user to the previous menu or perform any other desired action.
    pass

# Статус заказа



# Курс валют
@dp.callback_query_handler(lambda query: query.data == 'course')
async def handle_course(query: types.CallbackQuery):
    exchange_rate = 11.5  # Заменить фактическим обменным курсом

    message_text = f"Обменный курс:\n\n"
    message_text += f"Текущий курс на сегодняшний день 12.4\n"

    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("Ответы на популярные вопросы", callback_data='answers'),
        types.InlineKeyboardButton("Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)
    await query.message.reply(message_text, reply_markup=keyboard)

# Курс валют




# Ответы на популярные вопросы

@dp.callback_query_handler(lambda query: query.data == 'answers')
async def handle_answers(query: types.CallbackQuery):
    # Получите ответы на популярные вопросы из вашего источника данных или базы данных
    

    message_text = "Ответы на популярные вопросы:\n\n"
    message_text = "Если у вас появиться вопросы заходите по ссылке \n\n"
    message_text = "Переходи по ссылке\n\n"

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
