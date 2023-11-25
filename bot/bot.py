import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import requests
from django.utils import timezone 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.menu import get_menu_keyboard
from keyboards.menu import menu_buttons
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types
from openpyxl import Workbook
import psycopg2
import uuid
from django.db import transaction 
from states import CheckoutRetailState, CheckoutWholesaleState


def generate_item_id():
    # Generate a unique item ID using UUID (Universally Unique Identifier)
    item_id = str(uuid.uuid4())
    return item_id

workbook = Workbook()
sheet = workbook.active


conn = psycopg2.connect(
    host='coolbrs.com',
    port='5432',
    database='chyngyz',
    user='admin',
    password='C00lBRS123'
)
  



API_TOKEN = '5876031471:AAG15OS46lkP9X08u6OJWvMkFB3KJvxLKkg' 

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.reply('Приветствую! Рады, что вы воспользовались чат-ботом группы "Хороший Бизнес". Приятных заказов🤝', reply_markup=get_menu_keyboard())


@dp.callback_query_handler(lambda query: query.data == 'back', state='*')
async def process_back_callback(query: types.CallbackQuery, state: FSMContext):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    buttons = [
        types.InlineKeyboardButton("🛍️ Розничная торговля", callback_data='checkout_retail'),
        types.InlineKeyboardButton("📦 Оптовая торговля", callback_data='checkout_wholesale'),
        types.InlineKeyboardButton("⬅️ Назад", callback_data='back'),
    ]
    keyboard.add(*buttons)
    await query.message.edit_text('Meню', reply_markup=get_menu_keyboard())
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

# остановить заказ
@dp.message_handler(commands=['cancel'], state='*')
@dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logging.info('Cancelling state %r', current_state)
        await state.finish()
        await message.reply('Вы отменили текущее действие.')
# Оформить заказ


# Розничная торговля
@dp.callback_query_handler(lambda query: query.data == 'checkout_retail')
async def handle_checkout_retail(query: types.CallbackQuery):
    await bot.send_message(query.from_user.id, "Вы выбрали розничную торговлю.")
    await bot.send_message(query.from_user.id, "Введите свое имя пользователя в телеграмм через @, чтобы создать заказ:")
    await CheckoutRetailState.name.set()

@dp.callback_query_handler(lambda query: query.data == 'checkout_retail')
async def order_handler(message: types.Message):
    await CheckoutRetailState.first()
    await message.reply("Введите свое имя пользователя в телеграмм через @, чтобы создать заказ:")

@dp.message_handler(state=CheckoutRetailState.name)
async def process_name(message: types.Message, state: FSMContext):
    name = message.text.strip()
    if not name.startswith('@'):
        await message.reply("Имя пользователя должно начинаться с @. Пожалуйста, введите корректное имя пользователя.")
        return
    await state.update_data({'name': name})
    await CheckoutRetailState.next()
    await message.reply("Введите артикул C POIZON:")

@dp.message_handler(state=CheckoutRetailState.sku)
async def process_sku(message: types.Message, state: FSMContext):
    sku = message.text.strip()
    await state.update_data({'sku': sku})
    await CheckoutRetailState.next()
    await message.reply("Введите цвет товара:")

@dp.message_handler(state=CheckoutRetailState.color)
async def process_color(message: types.Message, state: FSMContext):
    color = message.text.strip()
    await state.update_data({'color': color})
    await CheckoutRetailState.next()
    await message.reply("Введите размер:")

@dp.message_handler(state=CheckoutRetailState.size)
async def process_size(message: types.Message, state: FSMContext):
    size = message.text.strip()
    await state.update_data({'size': size})
    await CheckoutRetailState.next()
    await message.reply("Введите сумму:")

@dp.message_handler(state=CheckoutRetailState.amount)
async def process_amount(message: types.Message, state: FSMContext):
    amount_in_yuan = message.text.strip()

    exchange_rate = 9.6  
    amount_in_rubles = float(amount_in_yuan) * exchange_rate

    await state.update_data({'amount': amount_in_yuan})
    await CheckoutRetailState.next()

    data = await state.get_data()
    name = data['name']
    sku = data['sku']
    color = data['color']
    size = data['size']
    amount_in_yuan = data['amount']
    amount_in_rubles = amount_in_rubles 
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

@dp.message_handler(content_types=types.ContentType.PHOTO, state=CheckoutRetailState.photo)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    data = await state.get_data()
    name = data['name']
    sku = data['sku']
    color = data['color']
    size = data['size']
    amount = data['amount']

    order_data = {
        'name': name,
        'sku': sku,
        'color': color,
        'size': size,
        'amount': amount,
        'photo': f"/media/photos/{photo_id}",
        'id_wh': generate_item_id(),
    }
    cur = conn.cursor()


    insert_query = """
    INSERT INTO telegram_retailorder (name, sku, color, size, amount, photo, id_wh)
    VALUES (%(name)s, %(sku)s, %(color)s, %(size)s, %(amount)s, %(photo)s, %(id_wh)s);
    """

    cur.execute(insert_query, order_data)


    conn.commit()
    cur.close()
    conn.close()


    
    await message.reply("Заказ успешно размещен. Спасибо, мы скоро свяжемся с вами!", reply_markup=types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True).add(
    types.KeyboardButton("Меню")
))


@dp.message_handler(commands=['cancel'], state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is not None:
        logging.info(f"Cancelling state {current_state}")
        await state.finish()  # Сбрасываем текущее состояние пользователя
        await message.reply("Вы отменили текущее действие. Можете начать заново.")
    else:
        await message.reply("Нет активных действий для отмены.")


# Оптовая торговля
@dp.callback_query_handler(lambda query: query.data == 'checkout_wholesale')
async def handle_checkout_wholesale(query: types.CallbackQuery):
    await CheckoutWholesaleState.first()
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
    await message.reply("Введите артикул  цвет кнопки для каждого товара, разделяя их по строкам. Например:\n"
                        "DD1903-100 Синяя \n"
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

async def process_size(message: types.Message, state: FSMContext):
    sizewh = message.text.strip()

    await state.update_data(sizewh=sizewh)
    await CheckoutWholesaleState.next()
    await message.reply("Введите общую сумму заказа в юанях:")

@dp.message_handler(state=CheckoutWholesaleState.amountwh)
async def process_amount(message: types.Message, state: FSMContext):
    amountwh = message.text.strip()

    await state.update_data(amountwh=amountwh)
    await CheckoutWholesaleState.next()

    # Retrieve the data from the state
    data = await state.get_data()
    username = data['username']
    quantitywh = data['quantitywh']
    items_data = data['items_data']
    amountwh = data['amountwh']

    # Prepare the message text
    message_text = f"👤 Пользователь: {username}\n"
    message_text += f"🛍️ Количество позиц ий: {quantitywh}\n"
    message_text += "📋 Детали заказа:\n"

    # Loop through items_data and add details for each item
    for i, (sku, color) in enumerate(items_data, start=1):
        message_text += f"Товар {i}:\n"
        message_text += f"  🏷️ Артикул C POIZON: {sku}\n"
        message_text += f"  🎨 Цвет кнопки: {color}\n"

    message_text += f"💰 Общая сумма заказа: {amountwh} юани\n"
    message_text += "🔗 Перейдите по ссылке для оплаты: [Оплатить](https://example.com)\n"
    message_text += "📷 После оплаты присылайте чек/фото перевода.\n"
    message_text += "✉️ Отправьте скриншот оплаты.\n"

    # Send the message to the user
    await message.reply(message_text, parse_mode="Markdown")

    # Move to the next state to handle photo confirmation
    await CheckoutWholesaleState.photowh.set()
    await message.reply("Пожалуйста, отправьте фото в качестве подтверждения оплаты.")

@dp.message_handler(content_types=types.ContentType.PHOTO, state=CheckoutWholesaleState.photowh)
async def process_photo(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id

    data = await state.get_data()
    username = data['username']
    quantity = data['quantitywh']
    items_data = data['items_data']
    amountwh = data['amountwh']

    try:
        # Соединение с базой данных
        conn = psycopg2.connect(
            host='localhost',
            port='5432',
            database='telebot',
            user='telebot',
            password='xsyusp'
        )

        # Создание курсора
        cursor = conn.cursor()

        # SQL-запрос для вставки данных
        insert_query = "INSERT INTO telegram_wholesaleordertelegtam (username, quantity, items_data, amountwh, photowh) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (username, quantity, items_data,  amountwh, photo_id))

        # Подтверждение изменений и закрытие соединения
        conn.commit()
        cursor.close()
        conn.close()

        await message.reply("Заказ успешно размещен. Спасибо, мы скоро свяжемся с вами!")
    except Exception as e:
        await message.reply(f"Произошла ошибка при сохранении данных: {str(e)}")







if __name__ == '__main__':
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
