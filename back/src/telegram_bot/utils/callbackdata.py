from aiogram.filters.callback_data import CallbackData


class ReturnToMenu(CallbackData):
    back: bool


class Profile(CallbackData):
    action: str


class OperationType(CallbackData, prefix="operation"):
    operation_type: str


class TikkerName(CallbackData, prefix="tikker"):
    tikker: str


class DisplayPrice(CallbackData, prefix="display"):
    tikker: str


class Verification(CallbackData, prefix="verif"):
    verif: bool


class CreditCard(CallbackData, prefix="ccnum"):
    cc_num: int


class CryptoWallet(CallbackData, prefix="cw_num"):
    cw_num: str


class CreditCardOwner(CallbackData, prefix="ccowner"):
    cc_owner: str
