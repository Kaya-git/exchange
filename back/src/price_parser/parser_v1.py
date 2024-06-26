from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


async def get_prices(ids, vs_currencies):

    return await cg.get_price(
        ids=ids,
        vs_currencies=vs_currencies
    )
