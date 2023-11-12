# Криптовалютный обменник 

## Описание:

«VVS-Coin»
Сервис для обмена криптовалютных активов на фиатные деньги и обратно. Пользователь может осуществовлять обмен без регистрации,
но необходимо будет приложить фото подтверждение владения кредитной карты с которой будет происходить обмен.
При регистрации, пользователь сможет увидеть историю своих завершенных обменов и участвовать в реферальной программе.

## Пользовательские роли
| Функционал                                                                                                                | Неавторизованные пользователи |  Авторизованные пользователи | Администратор |
|:--------------------------------------------------------------------------------------------------------------------------|:---------:|:---------:|:---------:|
| Доступна главная страница.                                                                                                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма авторизации                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма обмена                                                                                          | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма регистрации.                                                                                    | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница faq                                                                                                     | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница соглашения                                                                                              | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница резервов                                                                                                | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница тарифов                                                                                                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница отзывов                                                                                                 | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма отзыва                                                                                          | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница контактов                                                                                               | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна страница «История моих ордеров»                                                                                  | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает форма изменения пароля                                                                                | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна возможность выйти из системы (разлогиниться)                                                                     | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Доступна и работает система восстановления пароля.                                                                        | :x: | :heavy_check_mark: | :heavy_check_mark: |
| Изменять пароль любого пользователя.                                                                                      | :x: | :x: | :heavy_check_mark: |
| Блокировать/удалять аккаунты  и платежные средства пользователей.                                                         | :x: | :x: | :heavy_check_mark: |
| Верифицировать аккаунты и платежные средства пользователей.                                                               | :x: | :x: | :heavy_check_mark: |

## Администратор и админ-зона
:one: Все модели выведены в админ-зону с возможностью редактирования и удаление записей.  
:two: Для модели пользователей включена фильтрация списка по имени и email.  
:three: Для модели заказов включена фильтрация по айди и почте.  
:four: На моделе пользователя можно посмотреть общую сумму обмена.

## Запуск проекта

- Клонировать репозиторий GitHub (не забываем создать виртуальное окружение и установить зависимости):
[https://github.com/Kaya94/exchange](https://github.com/Kaya-git/exchange)

- Создать файл .env в папке проекта:
```
# Datababse
DB_USER=ЮЗЕР_БД
DB_HOST=ХОСТ_БД
DB_PASS=ПАРОЛЬ_БД
DB_NAME=ИМЯ_БД
DB_PORT=ПОРТ_БД

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Debug and logging
LOGGING_LEVEL=УРОВЕНЬ_ЛОГИРОВАНИЯ

# Admin secret_key
SECRET_KEY=СЕКРЕТКА

# Yadisk token
YADISKTOKEN=ТОКЕН_ЯНДЕКС_ДИСКА

#AdminAuth
ADMIN_AUTH=ПАРОЛЬ_АДМИНА

# JWT
# A constant secret which is used to encode the token.
SECRET_JWT=СЕКРЕТКА_JWT

#User Menager secret
SECRET_USER_MENAGER=ВАША_СЕКРЕТКА
```
- Собираем контейнеры:
```
docker-compose up -d --build
```
## Использованные технологии:
- Python 3.11
- FAST API: 0.101
- Redis: 5.0
- SQLAlchemy: 2.0
- Yanex Disk: 1.4
- SQLAdmin: 0.15
- Docker: 6.1
- FastApi Users: 12.1
- FastApi Storages: 0.2
- Pydantic: 2.1
- Alembic: 1.11
### Автор проекта:
- За Бэкенд Евгений Бузуев . С моими другими работами вы можете ознакомится по ссылке: https://github.com/SurfimChilim

