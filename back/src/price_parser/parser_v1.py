from pycoingecko import CoinGeckoAPI


cg = CoinGeckoAPI()


async def get_prices(coins, fiat_curr):

    return cg.get_price(
        ids=coins,
        vs_currencies=fiat_curr,
        include_market_cap=True,
        include_24hr_vol=True,
        include_24hr_change=True,
        include_last_updated_at=True
    )
