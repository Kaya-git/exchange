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
        cookies_id: str,
        email: str,
        send_value: float,
        send_curr: str,
        get_value: float,
        get_curr: str,
        cc_num: int,
        cc_holder: str,
        wallet_num: str
    ):
        await self.redis_conn.lpush(
            f"{cookies_id}",
            f"{email}",
            f"{send_value}",
            f"{send_curr}",
            f"{get_value}",
            f"{get_curr}",
            f"{cc_num}",
            f"{cc_holder}",
            f"{wallet_num}"
        )
        await self.redis_conn.expire(name=f'{cookies_id}', time=900)
        self.redis_conn.close


class Services:
    redis_values = RedisValues()


services = Services()
