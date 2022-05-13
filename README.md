# YaMDb API
## Проект YaMDb собирает отзывы пользователей на различные произведения.
Проект 10 спринта курса Python-разработчик [Яндекс.Практикум](https://practicum.yandex.ru/)

### Описание проекта:
Произведения делятся на категории: «Книги», «Фильмы», «Музыка». Список категорий может быть расширен администратором.
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Произведению может быть присвоен жанр из списка предустановленных (например, «Сказка», «Рок» или «Артхаус»). Новые жанры может создавать только администратор.
Пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — рейтинг (целое число). На одно произведение пользователь может оставить только один отзыв.

### Технологии в проекте:
- Python 3.7.9
- Django 2.2.16
- Django REST Flamework 3.12.4

### Как запустить проект:

Команды для запуска в коммандной строке:

```
git clone git@github.com:Banes31/api_yamdb.git
```

```
cd api_yamdb
```

Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```

> для Linux
```
source venv/bin/activate
```

> для Windows
```
source venv/Script/activate
```

Установите pip

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python manage.py migrate
```

Запустить проект:

```
python manage.py runserver
```

### OpenAPI

После установки доступен OpenAPI Redoc. Фейс доступен по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

### Регистрирация новых пользователей:
1. Пользователь отправляет POST-запрос на создание нового пользователя с параметрами *email* и *username* на [эндпоинт](http://127.0.0.1:8000/api/v1/auth/signup).
2. Сервис **YaMDB** отправляет письмо с кодом подтверждения (```confirmation_code```) на указанный адрес *email*.
3. Пользователь отправляет POST-запрос с параметрами *username* и *confirmation_code* на [эндпоинт](http://127.0.0.1:8000/api/v1/auth/token/), в ответе на запрос ему приходит *token* (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом.
После регистрации и получения токена пользователь может отправить PATCH-запрос на [эндпоинт](http://127.0.0.1:8000/api/v1/users/me/) и заполнить поля в своём профайле (описание полей — в документации).

# Авторы
Проект совместной работы авторов:
https://github.com/Banes31
https://github.com/Upr82
https://github.com/Grigorichev
