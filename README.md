# Foodgram - Продуктовый помошник

###

- Сервис позволяет зарегистрированным пользователям публиковать, редактировать и удалять рецепты.
- Пользователи могут подписываться/отписываться на/от интересных авторов, добавлять/удалять понравившиеся рецепты в избранное, а также в корзину.
- Доступна регистрация и аутентификация пользователей.

## **Технологии**

Django  
Django Rest Framework  
Docker  
Nginx  
Gunicorn  
Postgres

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

<!-- 4. Внутри контейнера backend выполнить команду для заполнения БД тестовыми данными

```
docker-compose exec backend python manage.py import_data
```

5. Чтобы сделать резервную копию базы данных, выполните команду

```
docker-compose exec backend python manage.py dumpdata > fixtures.json
```

### _Описание шаблона .env_

Необходимо указать переменные окружения в следующем формате:

DB_ENGINE=_СУБД_
DB_NAME=_имя БД_
POSTGRES_USER=_логин для подключения к БД_
POSTGRES_PASSWORD=_пароль для подключения к БД_
DB_HOST=_название сервиса (контейнера)_
DB_PORT=_порт для подключения к БД_
SECRET_KEY = _уникальный секретный ключ Django_ -->

## Автор: Домрачев Дмитрий [Dodmanat](https://github.com/Dodmanat)
