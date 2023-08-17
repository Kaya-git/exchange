from binance import AsyncClient
from config import conf
from pprint import pprint


class Parser:
    async def find_price(ticker: str) -> float:
        try:
            client = await AsyncClient.create(
                api_key=conf.parser.api_key,
                api_secret=conf.parser.secret_key_binance,
            )
            depth = await client.get_order_book(symbol=ticker)
            price = float(depth["bids"][0][0])
            print(f"Цена в рублях за один литкоин: {price}")
            return price
        finally:
            await client.close_connection()
