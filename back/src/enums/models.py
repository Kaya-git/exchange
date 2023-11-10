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


class CryptoType(enum.Enum):
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
    verify_new_order = "Необходимо верифицировать клиента и его платежные средства"
    verify_transaction = "Клиент оплатил заказ. Необходимо верифицировать платеж и провести оплату"
    verify_review = "Необходимо валидировать новый отзыв"
