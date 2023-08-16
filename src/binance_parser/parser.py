from binance import AsyncClient
from config import conf


class Parser:
    async def find_price(ticker):
        try:
            client = await AsyncClient.create(
                api_key=conf.parser.api_key,
                api_secret=conf.parser.secret_key_binance,
            )
            depth = await client.get_order_book(symbol=ticker)
            price = depth["bids"][0][0]
            return float(price)
        finally:
            await client.close_connection()
