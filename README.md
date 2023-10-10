# exchange
crypto_exchange

## Запуск проекта

- Клонировать репозиторий https://github.com/Kaya94/exchange

- Установить и активировать виртуальное окружение    
```
Для пользователей Windows:
python -m venv venv
source venv/Scripts/activate
python -m pip install --upgrade pip
```
- Установить зависимости из файла requirements.txt
```
pip install -r requirements.txt
```
 - Создать .env и записать в него следующие значения:
# Datababse
DB_USER=postgres
DB_HOST=localhost
DB_PASS=ПАРОЛЬ
DB_NAME=new_exchange
DB_PORT=5432

# Redis
REDIS_DATABASE=1
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=ПАРОЛЬ
REDIS_USERNAME=kaya

# Debug and logging
LOGGING_LEVEL=1

# Admin secret_key
SECRET_KEY=Ezjell

# Binance API
BINANCE_API_KEY=БИНАНС АПИ КЛЮЧ
SECRET_KEY_BINANCE=СЕКРЕТ БИНАНС

# Yadisk token
YADISKTOKEN=ТОКЕН ЯНДЕКС ДИСКА

#AdminAuth
ADMIN_AUTH=WW9JUQhP

# JWT
# A constant secret which is used to encode the token.
SECRET_JWT=SECRET

#User Menager secret
SECRET_USER_MENAGER=WW9JUQhP
```
-Заресторить дамп бд через pgadmin
```
- Установить и запустить редис на ubuntu
```
redis-server --daemonize yes
```
- переходим в src и запускаем main.py
```
py main.py
```
И полюбому что то пойдет не так
