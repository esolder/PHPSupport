# PHPSupport backend

## Установка
Установите зависимости:
```
pip install -r requirements.txt
```
Создайте `.env` файл и добавьте туда следующие данные:
- `CLIENT_BOT_TOKEN` - токен бота для клиентов
- `EXECUTOR_BOT_TOKEN` - токен бота для подрядчиков

Создайте миграции проекта:
```
python manage.py makemigrations
```
Создайте миграции приложения:
```
python manage.py makemigrations controller
```
Проведите миграции:
```
python manage.py migrate
```
Создайте суперпользователя:
```
python manage.py createsuperuser
```

## Работа с API

Заполните в админке тестовые данные (обязательно добавьте хотя бы одну ставку)

Пробуем получить всех клиентов:
```python
import requests

url = 'http://127.0.0.1:8000/clients/'

response = requests.get(url, auth=('superuser_login', 'superuser_password'))
response.raise_for_status()
print(response.content)
```

### Бот клиента
#### Получить клиента по username
```
GET /client/
``` 
Параметры:
`username` (обязательный) - уникальный telegram username

Пример ответа:
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "username": "Esolder",
    "subscription_end": "2023-02-24"
}
```
Если указанного юзера нет в базе, то вернётся пустой `json` объект

#### Запрос с заявкой на доработку сайта
```
POST /orders/
```
Пример данных в заказе:
```json
{
    "id": 1,
    "client": "http://127.0.0.1:8000/clients/2/",
    "client_tg_id": 123123,
    "creation_date": "2023-02-20",
    "text": "asda",
    "executor": null,
    "executor_tg_id": null,
    "questions": null,
    "answers": null,
    "is_taken": false,
    "credentials": "bla",
    "is_complete": false,
    "rate": "http://127.0.0.1:8000/rates/2/",
    "estimate": null,
    "complete_date": null
}
```
Обратите внимание: client, rate, executor - это ссылки на объекты.

При составлении `POST` запроса для данного кейса нужно указать ссылку на клиента, id клиента в telegram и текст заказа.

#### Запрос с отправкой секретных ключей
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно передавать credentials.

#### PATCH с ответами на вопросы
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно передавать answers.




### Бот подрядчика
#### Получить подрядчика по username
```
GET /executor/?username=<tlg_username>
``` 
Пример ответа:
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "username": "Vasya"
}
```
Если указанного юзера нет в базе, то вернётся пустой `json` объект

#### Получить текущую ставку
```
GET /actual-rate/
```
Пример ответа:
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 3,
    "rate": "2500.00",
    "when_set": "2023-02-17T09:58:57.581724+03:00"
}
```
#### Получить свободные заказы
```
GET /orders/?free=True
```
Пример ответа:
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept
{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "client": "http://127.0.0.1:8000/clients/2/",
            "client_tg_id": 123123,
            "creation_date": "2023-02-20",
            "text": "asda",
            "executor": null,
            "executor_tg_id": null,
            "questions": null,
            "answers": null,
            "is_taken": false,
            "credentials": "bla",
            "is_complete": false,
            "rate": "http://127.0.0.1:8000/rates/2/",
            "estimate": null,
            "complete_date": null
        }
    ]
}
```
Максимальное количество результатов на одной странице ответа - 10
#### Бронирование заказа
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно указать ссылку на подрядчика, id подрядчика в telegram.

#### post с уточняющими вопросами
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно передавать questions.
#### Отправить эстимейт
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно указать эстимейт.

#### Взять заказ
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно установить `is_taken` в значение `True`.

#### Закрыть заказ
```
PATCH /orders/<id заказа>/
```
При составлении `PATCH` запроса для данного кейса нужно установить `is_complete` в значение `True`.
