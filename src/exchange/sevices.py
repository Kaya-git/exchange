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
        await self.redis_conn.expire(f'{email}', 300)
        self.redis_conn.close


# Очередь для сохранения pending_order_emails
class EmailQueue:
    def __init__(self):
        self.queue = []

    async def push(self, item):
        self.queue.append(item)

    async def pop(self):
        if len(self.queue) == 0:
            return None
        removed = self.queue.pop(0)
        return removed


class Services:
    email_queue = EmailQueue()
    redis_values = RedisValues()


services = Services()
