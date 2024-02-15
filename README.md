# Foodgram

![GITHUB-BADGE](https://github.com/ConstantineGolovin/foodgram-project-react/workflows/main/badge.svg)

Социальная сеть в которой можно делиться своими рецептами, а также находить новые рецепты для себя у других пользователей. Также, на этом сервисе есть удобная возможность добавлять рецепты в избранное или список покупок, в котором можно скачать список необходимых ингредиентов.

## Использованные технологии
* Docker
* DRF
* Djoser
* GitHub Actions
* Pillow
* PostgreSQL

## Запуск проекта через Docker
Клонировать репозиторий:
~~~
git clone git@github.com:ConstantineGolovin/foodgram-project-react.git
~~~
Запуск проекта:
~~~
sudo docker compose -f docker-compose.production.yml up
~~~
Зайти в контейнер backend, запустить в нём миграции, собрать статику, создать суперпользователя, загрузить ингредиенты:
~~~
sudo docker compose -f docker-compose.production.yml exec backend bash
./manage.py makemigrations
./manage.py migrate
./manage.py collectstatic
./manage.py createsuperuser
./manage.py load_ingredients
~~~

## Доменное имя проекта
recipesmythorn.ddns.net

## Вход в админку
email: admin@mail.ru
password: admin

## Автор проекта
Головин К.А., 70 когорта


