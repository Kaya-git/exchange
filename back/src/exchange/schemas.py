# from pydantic import BaseModel
# from decimal import Decimal
# from fastapi import Form

# # class ExchangeRates(BaseModel):
# #     client_sell_tikker_id: int
# #     client_buy_tikker_id: int


# class FillOrederForm(BaseModel):
#     client_sell_value: Decimal = Form(default=0),
#     client_sell_tikker_id: int = Form(),
#     client_buy_value: Decimal = Form(default=0),
#     client_buy_tikker_id: int = Form(),
#     client_email: str = Form(),
#     client_crypto_wallet: str = Form(),
#     client_credit_card_number: str = Form(),
#     client_cc_holder: str = Form(),

# class ConfirmOrder(BaseModel):
#     ...

# class ConfermCC(BaseModel):
#     ...

# class AwaitConformation(BaseModel):
#     ...

# class Requisites(BaseModel):
#     ...

# class PayedButton(BaseModel):
#     ...
