![Workflow Foodgram](https://github.com/dodmanat/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master&event=push)

# Foodgram - Продуктовый помошник

## Адрес

http://51.250.25.57/

## Админка

    login - admin
    password - admin

###

- Сервис позволяет зарегистрированным пользователям публиковать, редактировать и удалять рецепты.
- Пользователи могут подписываться/отписываться на/от интересных авторов, добавлять/удалять понравившиеся рецепты в избранное, а также в корзину.
- Доступна регистрация и аутентификация пользователей.

## **Технологии**

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## **Запуск проекта**

Выполните следующие команды в терминале:

1. Клонировать проект из репозитория

```
git clone https://github.com/DoDmAnat/foodgram-project-react
```

2. Перейти в папку infra и создать файл «.env», добавив в него переменные окружения.

```
cd infra
```

```
touch .env
```

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=<ваш_django_секретный_ключ>
```

3. Выполнить команду запуска docker-compose в «фоновом режиме»

```
docker-compose up -d --build
```

После сборки контейнеров необходимо подготовить БД, выполнив следующее:

1. Внутри контейнера backend выполнить миграции

```
docker-compose exec backend python manage.py migrate
```

2. Внутри контейнера backend создать суперпользователя

```
docker-compose exec backend python manage.py createsuperuser
```

3. Внутри контейнера backend выполнить команду сбора статики

```
docker-compose exec backend python manage.py collectstatic --no-input
```

4. Внутри контейнера backend выполнить команду для заполнения БД тестовыми данными

```
docker-compose exec backend python manage.py import_data
```

5. Для загрузки данных в базу выполнить команду:

```
docker-compose exec foodgram_backend python manage.py loaddata data/fixtures.json
```
### Примеры запросов

### Регистрация нового пользователя:

```bash
POST - 'http://localhost/api/users/'
```
```yaml
{
  "username": "user_username.",
  "email": "user@mail.ru",
  "password": "user_password.",
  "first_name": "user_first_name",
  "last_name": "user_last_name"
}
```

#### Ответ
```yaml
{
  "id": 2,
  "username": "user_username.",
  "email": "user@mail.ru",
  "first_name": "user_first_name",
  "last_name": "user_last_name"
}
```

### Получение токена:
#### Запрос
```bash
POST - 'http://localhost/api/auth/token/login/'
```
```yaml
{
  "password": "user_password.",
  "email": "user@mail.ru"
}
```

#### Ответ
```yaml
{ "auth_token": "token_value" }
```

### Информация о своей учетной записи:
#### Запрос
```bash
GET - 'http://localhost/api/users/me/'
header 'Authorization: Token "token_value"'
```

#### Ответ
```yaml
{
  "id": 2,
  "username": "user_username.",
  "email": "user@mail.ru",
  "first_name": "user_first_name",
  "last_name": "user_last_name",
  "is_subscribed": false
}
```

### Добавление нового рецепта:
#### Запрос
```bash
POST - 'http://localhost/api/recipes/'
header 'Authorization: Token "token_value"'
```
```yaml
{
  "ingredients": [
    {
      "id": 11,
      "amount": 270
    },
    {
      "id": 38,
      "amount": 2
    },
    {
      "id": 267,
      "amount": 30
    },
  ],
  "tags": [
    1,
    2
  ],
  "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
  "name": "Название рецепта",
  "text": "Описание рецепта",
  "cooking_time": 15
}
```

#### Ответ
```yaml
{
  "id": 4,
  "tags": [
    {
      "id": 1,
      "name": "Завтрак",
      "color": "#E26C2D",
      "slug": "breakfast"
    },
    {
      "id": 2,
      "name": "Обед",
      "color": "#0000CD",
      "slug": "dinner"
    }
  ],
  "author": {
    "id": 2,
    "username": "user_username.",
    "email": "user@mail.ru",
    "first_name": "user_first_name",
    "last_name": "user_last_name",
    "is_subscribed": false
  },
  "ingredients": [
    {
      "id": 11,
      "name": "Вода",
      "measurement_unit": "мл",
      "amount": 270
    },
    {
      "id": 38,
      "name": "Сахар",
      "measurement_unit": "ч. ложка",
      "amount": 2
    },
    {
      "id": 267,
      "name": "Молоко",
      "measurement_unit": "мл",
      "amount": 30
    }
  ],
  "is_favorited": false,
  "is_in_shopping_cart": false,
  "name": "Название рецепта",
  "image":"http://foodgram.example.org/media/recipes/images/image.jpeg",
  "text": "Описание рецепта.",
  "cooking_time": 15
}
```
[API документация](http://51.250.25.57/api/docs/redoc.html)

## Автор: Домрачев Дмитрий [Dodmanat](https://github.com/Dodmanat)
