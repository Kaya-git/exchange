from binance_parser import Parser
from database.db import Database


# Constants with price on binance
LTC_PRICE = Parser.find_price("LTCRUB")
BTC_PRICE = Parser.find_price("BTCRUB")

# Constants with commissions
MARGIN = 7 or Database.commissions.get(ident=(id == 1)).margin
GAS = 130 or Database.commissions.get(ident=(id == 1)).gas
