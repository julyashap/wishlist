# Wishlist App

Простой веб-сервис для создания и управления списками желаний (вишлистов).

## Стек технологий
- **Backend:** Python, FastAPI, SQLAlchemy, PyJWT
- **Database:** PostgreSQL
- **Frontend:** HTML, JavaScript, Bootstrap

## Переменные окружения

Для локального запуска приложения создайте файл `.env` в корневой директории проекта и заполните его следующими переменными:

```env
# Настройки подключения к PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=my_secure_password
POSTGRES_DB=wishlist
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

# Секретный ключ для авторизации (JWT)
SECRET_KEY=secret_key
```

## Инструкция по запуску

1. Установите Docker и Docker Compose
2. Перейдите в корень проекта
3. Запустите команду: `docker-compose up`
4. Теперь можете перейти на сайт по адресу: `http://0.0.0.0:8000`
