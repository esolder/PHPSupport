# PHPSupport backend

## Установка
Установите зависимости:
```
pip install -r requirements.txt
```
Создайте миграции проекта:
```
python manage.py makemigrations
```
Создайте миграции приложения:
```
python manage.py makemigration controller
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

Заполните в админке тестовые данные

Пробуем получить всех клиентов:
```python
import requests

url = 'http://127.0.0.1:8000/сlients/'

orders = requests.get(url, auth=('superuser_login', 'superuser_password'))
print(orders.content)
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
    "client": "http://127.0.0.1:8000/clients/1/",
    "executor": null,
    "is_taken": false,
    "is_complete": false,
    "rate": "http://127.0.0.1:8000/rates/2/",
    "estimate": null,
    "complete_date": null,
    "text": "gg"
}
```
Обратите внимание: client, rate, executor - это ссылки на объекты.

При составлении `POST` запроса для данного кейса нужно указать ссылку на клиента и текст заказа.

#### POST запрос с отправкой секретных ключей
TODO

#### PUT с ответами на вопросы
TODO




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
            "client": "http://127.0.0.1:8000/clients/1/",
            "executor": null,
            "is_taken": false,
            "is_complete": false,
            "rate": "http://127.0.0.1:8000/rates/2/",
            "estimate": null,
            "complete_date": null,
            "text": "gg"
        }
    ]
}
```

#### Бронирование заказа
```
PUT /orders/<id заказа>/
```
При составлении `PUT` запроса для данного кейса нужно указать ссылку на подрядчика.

#### post с уточняющими вопросами
TODO
#### Отправить эстимейт
```
PUT /orders/<id заказа>/
```
При составлении `PUT` запроса для данного кейса нужно указать эстимейт.

#### Взять заказ
```
PUT /orders/<id заказа>/
```
При составлении `PUT` запроса для данного кейса нужно установить `is_taken` в значение `True`.

#### Закрыть заказ
```
PUT /orders/<id заказа>/
```
При составлении `PUT` запроса для данного кейса нужно установить `is_complete` в значение `True`.
