# abol
Тестовое задание для Аболъ


2 приложения:
    - web - сервис для операций над книгами.
    Реализован на стеке FastAPI, uvicorn, pydantic, alembic, postgresql
    После запуска на localhost:8000/docs доступна документация, а также можно 
    проверить работу сервиса. 
    для доступа к эндпоинтам книг необходимо создать пользователя и зарегистрироваться
    (пароль не короче 6 символов, хотя бы одна буква и цифра)
    при запросах со стороны внешних сервисов необходимо получить токен
    - grpc - сервис для получения данных о книгах. Возможно получение данных о конкретной книге 
    или списка книг с пагинацией.
    прото-файл лежит в /grpc/protobufs/books.proto
    использовались grpcio,  grpcio-tools, psycopg2
    доступен, например, из postman, в котором при создании новой вкладки необходимо 
    выбрать grpc, перенести прото-файл. доступ на localhost:50051, методы SingleBook, BookList
    - 2 бд, основная и тестовая. тесты для обоих сервисов написаны на pytest
    - брокер сообщений rabbitmq, админка доступна на http://172.21.0.2:15672 "guest:guest"

Запуск с помощью docker-compose up -d --build

код проверен с помощью flake8 (увеличена длина строки с 79 до 119). импорты отсортированы isort
