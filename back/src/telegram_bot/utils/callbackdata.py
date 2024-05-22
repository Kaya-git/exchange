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
