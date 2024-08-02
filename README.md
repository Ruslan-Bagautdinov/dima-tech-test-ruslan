# FastAPI Приложение

Это FastAPI приложение предоставляет RESTful API для управления пользователями, счетами и платежами.

## Описание Эндпоинтов

- **POST /login** - Аутентификация пользователя и выдача токенов доступа и обновления. После успешной аутентификации пользователь получает:
  - **Access Token**: Используйте его для авторизации запросов через Swagger UI. Передайте Access Token в `Authorize`.
  - **Refresh Token**: Используйте его для обновления Access Token после истечения его срока действия (30 минут) через конечную точку `/refresh_token`.

  Для тестирования можно использовать следующие учетные данные:
  - **Администратор**: email: admin@example.com, пароль: 123
  - **Пользователь**: email: user@example.com, пароль: 456

- **POST /refresh_token** - Обновление Access Token с использованием Refresh Token. После истечения срока действия Access Token (30 минут), используйте эту конечную точку для получения нового Access Token.
  - **Refresh Token**: Передайте Refresh Token в теле запроса для обновления Access Token.

- **GET /user/me** - Получить информацию о текущем аутентифицированном пользователе.
- **GET /user/me/accounts** - Получить список счетов текущего аутентифицированного пользователя.
- **GET /user/me/payments** - Получить список платежей текущего аутентифицированного пользователя.
- **GET /users/all** - Получить список всех пользователей (только для администраторов).
- **POST /users/new** - Создать нового пользователя (только для администраторов).
- **GET /users/{user_id}** - Получить информацию о пользователе по его ID (только для администраторов).
- **PATCH /users/{user_id}** - Обновить информацию о пользователе по его ID (только для администраторов).
- **DELETE /users/{user_id}** - Удалить пользователя по его ID (только для администраторов).
- **GET /users/{user_id}/accounts** - Получить список счетов пользователя по его ID (только для администраторов).
- **POST /webhook** - Обработать вебхук для обработки платежа.
- **GET /generate_webhook_json** - Сгенерировать JSON для тестирования вебхука.

## Установка и Запуск с Использованием Docker Compose

1. **Клонируйте репозиторий:**

```sh
git clone https://github.com/your-repo/your-fastapi-app.git
cd your-fastapi-app
```

2. **Соберите и запустите контейнеры с помощью Docker Compose:**

```sh
docker-compose up --build
```

3. **Приложение будет доступно по адресу:**

```http
http://localhost:8000/
```

## Установка и Запуск Без Docker Compose

1. **Клонируйте репозиторий:**

```sh
git clone https://github.com/your-repo/your-fastapi-app.git
cd your-fastapi-app
```

2. **Создайте базу данных на вашем сервере PostgreSQL:**

```sql
CREATE DATABASE dima_tech_test;
CREATE USER postgres WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE dima_tech_test TO postgres;
```

3. **Создайте файл .env в корне проекта с соответствующими переменными окружения:**

```dotenv
POSTGRES_HOST='localhost'
POSTGRES_PORT='5432'
POSTGRES_DB='dima_tech_test'
POSTGRES_USER='postgres'
POSTGRES_PASSWORD='your_password'

SECRET_KEY='your_secret_key_here'
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_MINUTES=10080
ALGORITHM=HS256
```

4. **Установите зависимости:**

```sh
pip install -r requirements.txt
```

5. **Примените миграции Alembic:**

```sh
alembic upgrade head
```

6. **Запустите приложение:**

```sh
uvicorn main:app --host 0.0.0.0 --port 8000
```

7. **Приложение будет доступно по адресу:**

```http
http://localhost:8000/
```

### Тестовые Учетные Данные
- Администратор: email: admin@example.com, пароль: 123

- Пользователь: email: user@example.com, пароль: 456
