from decimal import Decimal
import requests


async def find_price(ids, vs_currencies) -> Decimal:
    base = 'https://api.coingecko.com'
    path = '/api/v3/simple/price'
    url = base + path

    param = {
        'ids': f'{ids}',
        'vs_currencies': f'{vs_currencies}'
    }
    data = requests.get(url=url, params=param)
    price = round(
        Decimal(data.json()[param['ids']][param['vs_currencies']]), 2
    )
    return price
