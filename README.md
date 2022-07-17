# Социальная сеть


### Описание
Данный проект представляет собой подобие социальной сети. Здесь есть главная страница, есть страница автора с его постами, а так же страница самого поста с комментариями к нему. Посты можно оставлять в тематических группах. Имеется возможность подписки на того или иного автора. Реализован полный функционал регистрации и восстановления пароля через почту.


### Технологии
Python 3.9
Django 2.2.16
Djangorestframework 3.12.4
Djangorestframework-simplejwt 4.7.2
Djoser 2.1.0


### Запуск проекта на локальном сервере
- Установите и активируйте виртуальное окружение
```py -m venv venv```
```. venv/Scripts/activate```

- Установите зависимости из файла requirements.txt
```pip install -r requirements.txt```

- Выполните все миграции
```py manage.py makemigrations```
```py manage.py migrate```

- В папке с файлом manage.py выполните команду:
```py manage.py runserver```


### Примеры запросов
**Пример GET-запроса: получить список всех публикаций.**
**При указании параметров limit и offset выдача с пагинацией.**
_GET .../api/v1/posts/_

**Пример ответа:**
```
{
    "count": 123,
    "next": "http://api.example.org/accounts/?offset=400&limit=100",
    "previous": "http://api.example.org/accounts/?offset=200&limit=100",
    "results": [
        {
            "id": 0,
            "author": "string",
            "text": "string",
            "pub_date": "2021-10-14T20:41:29.648Z",
            "image": "string",
            "group": 0
        }
    ]
}
```

**Пример POST-запроса с токеном: добавление нового поста.**
_POST .../api/v1/posts/_
```
    {
        "text": "string", -
        "image": "string",
        "group": 0
    } 
```
**Пример ответа:**
```
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "pub_date": "2019-08-24T14:15:22Z",
        "image": "string",
        "group": 0
    }
```

**Пример POST-запроса с токеном: отправляем новый комментарий к посту с id=14.**
_POST .../api/v1/posts/14/comments/_
```
    {
        "text": "string"
    } 
```
**Пример ответа:**
```
    {
        "id": 0,
        "author": "string",
        "text": "string",
        "created": "2019-08-24T14:15:22Z",
        "post": 14
    }
```

**Пример GET-запроса: получаем информацию о группе.**
_GET .../api/v1/groups/2/_

**Пример ответа:**
```
[
    {
        "id": 0,
        "title": "string",
        "slug": "string",
        "description": "string"
    }
]
```

**Пример POST-запроса с токеном: подписка пользователя на**
**другого пользователя переданного в теле запроса.**
_POST .../api/v1/follow/_
```
    {
        "following": "string"
    } 
```
**Пример ответа:**
```
    {
        "user": "string",
        "following": "string"
    }
```


#### Автор
Карапетян Зорик
РФ, Санкт-Петербург, Купчино.
