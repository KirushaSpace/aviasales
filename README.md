# aviasales

## Запускаем проект с использованием Docker и настройкой контейнеров
### Docker compose commands
*создание контейнеров и подключение всех библиотек*
```sh
docker-compose build
```
*миграция базы данных*
```sh
docker-compose run web alembic revision --autogenerate -m "mig"
```
```sh
docker-compose run web alembic upgrade head
```
*создание базовых сущностей*
```sh
docker-compose run web python app/init_data.py
```
*запуск контейнеров*
```sh
docker-compose up

*.env*
```sh
переименовать example.env в .env
```