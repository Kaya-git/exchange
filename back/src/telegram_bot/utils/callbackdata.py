from aiogram.filters.callback_data import CallbackData


class AccountInfo(CallbackData):
    action: str


class OperationInfo(CallbackData):
    operation: str
    tikker: str


class ValueIn(CallbackData):
    currency: str