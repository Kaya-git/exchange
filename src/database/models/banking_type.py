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
