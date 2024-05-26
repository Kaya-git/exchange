from aiogram.fsm.state import StatesGroup, State


class ExchangeStates(StatesGroup):
    user_uuid = State()
    operation_type = State()
    display_price = State()
    client_sell_tikker = State()
    client_sell_value = State()
    client_buy_tikker = State()
    client_buy_value = State()
    client_email = State()
    money_amount = State()
    client_credit_card_number = State()
    client_cc_holder = State()
    client_crypto_wallet = State()
