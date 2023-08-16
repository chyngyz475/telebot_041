from aiogram.dispatcher.filters.state import StatesGroup, State


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
    photowh = State() 
  
