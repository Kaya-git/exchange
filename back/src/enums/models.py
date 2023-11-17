import enum


class BankingType(enum.StrEnum):
    SBER = "SBER"
    CRYPTO = "CRYPTO"
    QIWIRUR = "QIWIRUR"
    QIWIUSD = "QIWIUSD"
    YAMONEY = "YAMONEY"
    PAYRUR = "PAYRUR"
    PAYUSD = "PAYUSD"
    PAYEUR = "PAYEUR"


class CurrencyType(enum.Enum):
    Crypto = "crypto"
    Fiat = "fiat"


class Mark(enum.IntEnum):
    one_star = 1
    two_stars = 2
    three_stars = 3
    four_stars = 4
    five_stars = 5


class Role(enum.StrEnum):
    User = "user"
    Moderator = "moderator"
    Admin = "admin"


class Status(enum.StrEnum):
    Pending = "pending"
    Timeout = "timeout"
    Canceled = "canceled"
    Inprocces = "inprocces"
    Approved = "approved"
    Completed = "completed"


class ReqAction(enum.StrEnum):
    VerifyNewOrder = "Необходимо верифицировать клиента и его платежные средства"
    VerifyTransaction = "Клиент оплатил заказ. Необходимо верифицировать платеж и провести оплату"
    VerifyReview = "Необходимо валидировать новый отзыв"


class VerifDeclineReason(enum.StrEnum):
   Last4Digits = "Не видно последние 4 цифры карты"
   WebDomen = "Не видно домен сайта"
   NoOrder = "Не видно номер заявки"
   Inittials = "Не видно ФИО"
   BadQuality = "Плохое качество фотографии"
