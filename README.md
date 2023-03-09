![Workflow Foodgram](https://github.com/dodmanat/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

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

5. Чтобы сделать резервную копию базы данных, выполните команду

```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```

[API документация](http://51.250.25.57.ru/docs/redoc.html)

## Автор: Домрачев Дмитрий [Dodmanat](https://github.com/Dodmanat)
