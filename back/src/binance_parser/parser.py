from config import conf
from decimal import Decimal
import requests


async def find_price(ticker: str) -> Decimal:
    base = 'https://api.binance.com'
    path = '/api/v3/depth'
    url = base + path
    param = {'symbol': f'{ticker}'}
    data = requests.get(url=url, params=param)
    price = Decimal(data.json()["bids"][0][0])
    print(price)
    return price