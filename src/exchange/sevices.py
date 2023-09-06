import redis.asyncio as redis
from config import conf


# Класс для пересчета операций с учетом маржи и комиссий
class Count:
    async def count_get_value(
        send_value,
        coin_price,
        margin, gas
    ):
        get_value = (
            (send_value - ((send_value * margin) / 100) - gas) / coin_price
        )
        return get_value

    async def count_send_value(get_value, coin_price, margin, gas):
        send_value = (
            (coin_price + ((get_value * margin) / 100) * get_value) + gas
        )
        return send_value


# Класс для работы с редис
class RedisValues:

    redis_conn = redis.Redis(host=conf.redis.host, port=conf.redis.port)

    async def set_order_info(
        self,
        user_id: str,
        client_email: str,
        client_send_value: float,
        send_tikker_id: int,
        client_get_value: float,
        get_tikker_id: str,
        client_cc_num: int,
        client_cc_holder_name: str,
        client_crypto_wallet: str
    ):
        await self.redis_conn.lpush(
            f"{user_id}",
            f"{client_email}",
            f"{client_send_value}",
            f"{send_tikker_id}",
            f"{client_get_value}",
            f"{get_tikker_id}",
            f"{client_cc_num}",
            f"{client_cc_holder_name}",
            f"{client_crypto_wallet}"
        )
        await self.redis_conn.expire(name=f'{user_id}', time=900)
        self.redis_conn.close


class Services:
    redis_values = RedisValues()


services = Services()
