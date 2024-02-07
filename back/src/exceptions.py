from fastapi import HTTPException, status


class ExchangeException(HTTPException):
    status_code = 500
    detail = ""

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(ExchangeException):
    status_code = (status.HTTP_409_CONFLICT,)
    detail = ("Пользователь уже существует",)


class IncorrectEmailOrPasswordException(ExchangeException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Неверная почта или пароль",)


class TokenExpiredException(ExchangeException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Токен истек",)


class TokenAbsentException(ExchangeException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Токен отсутствует",)


class IncorrectTokenException(ExchangeException):
    status_code = (status.HTTP_401_UNAUTHORIZED,)
    detail = ("Неверный формат токена",)


class UserIsNotPresentException(ExchangeException):
    status_code = status.HTTP_401_UNAUTHORIZED


class UserIsNotAdminException(ExchangeException):
    status_code = (status.HTTP_403_FORBIDDEN,)
    detail = ("Пользователь не является администратором",)


class DateFromWrongFormatException(ExchangeException):
    status_code = (status.HTTP_409_CONFLICT,)
    detail = ("Неверный формат даты, date_from >= date_to",)


class OutOfDateException(ExchangeException):
    status_code = (status.HTTP_409_CONFLICT,)
    detail = ("Неверные параметры даты",)
