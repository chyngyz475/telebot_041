from aiogram.dispatcher.filters.state import State,StatesGroup


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

    # Добавьте здесь другие состояния, используемые в вашем проекте
