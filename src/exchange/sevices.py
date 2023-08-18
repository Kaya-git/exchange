import redis.asyncio as redis
from config import conf


# Класс для пересчета операций с учетом маржи и комиссий
class Count:
    async def count_get_value(send_value, coin_price, margin, gas):
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

    async def set_email_values(
        self,
        email: str,
        send_value: float,
        get_value: float,
        cc_num: int,
        cc_holder: str,
    ):
        await self.redis_conn.lpush(
            f'{email}',
            f"{send_value}",
            f"{get_value}",
            f"{cc_num}",
            f"{cc_holder}",
        )
        await self.redis_conn.expire(name=f'{email}', time=300)
        self.redis_conn.close


class Services:
    redis_values = RedisValues()


services = Services()
