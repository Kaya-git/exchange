import httpx


async def ver_recaptcha(token: str, secret_key: str, url: str) -> bool:
    data = {'secret': secret_key, 'response': token}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, data=data)
            response.raise_for_status()

            return response.json()
        except httpx.RequestError as exc:
            return f"Произошла ошибка при запросе {exc.request.url!r}."
