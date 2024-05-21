from currencies.routers import currency_list


async def get_crypto() -> int:
    currency_lst = await currency_list()
    crypto_lst = []
    for i in currency_lst:
        if i["type"] == "Крипто-валюта":
            crypto_lst.append(i)
    return crypto_lst
