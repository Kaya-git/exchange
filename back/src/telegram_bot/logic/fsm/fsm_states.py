from aiogram.fsm.state import StatesGroup, State


class ExchangeStates(StatesGroup):
    user_uuid = State()
    end_point_number = State()
    client_email = State()
    client_sell_value = State()
    client_sell_tikker = State()
    client_buy_value = State()
    client_buy_tikker = State()
    client_credit_card_number = State()
    client_cc_holder = State()
    client_crypto_wallet = State()
