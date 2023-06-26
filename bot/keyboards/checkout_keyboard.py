from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher.filters.state import State, StatesGroup

from main import dp, conn, sheet, workbook

class CheckoutRetailState(StatesGroup):
    name = State()
    sku = State()
    color = State()
    size = State()
    amount = State()
    photo = State()

@dp.callback_query_handler(lambda query: query.data == 'checkout_retail')
async def handle_checkout_retail(query: types.CallbackQuery):
    await CheckoutRetailState.first()
    await query.message.reply("Введите свое имя и фамилию, чтобы создать заказ:")

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

    message_text = f"Подтверждение заказа:\n\n"
    message_text += f"Full Name: {name}\n"
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

    # Close the cursor
    cursor.close()

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
