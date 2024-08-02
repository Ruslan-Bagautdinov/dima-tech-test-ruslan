from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from routers.admin import router as admin_router
from routers.auth import router as auth_router
from routers.login import router as login_router
from routers.user import router as users_router
from routers.webhook import router as webhook_router

description = """
Добро пожаловать в API аутентификации и управления пользователями на FastAPI!

Этот API позволяет вам:
- Аутентифицировать пользователей. Получать и обновлять токены доступа.
- Управлять пользователями.
- Обрабатывать вебхуки для платежных транзакций. Генерировать json для тестирования обработки вебхуков.

#### Роли
- **Администратор**: Может управлять всеми пользователями (создание, чтение, обновление, удаление пользователей).
    Может получать списки пользователей и списки их счетов с балансами.
- **Пользователь**: Может просматривать свои данные, свои счета и балансы и список своих транзакций.

"""

app = FastAPI(
    title="API аутентификации и управления пользователями на FastAPI",
    description=description,
    version="1.0.0"
)

app.include_router(auth_router, tags=["Аутентификация"])
app.include_router(login_router, tags=["Вход"])
app.include_router(admin_router, tags=["Администратор"])
app.include_router(users_router, tags=["Пользователи"])
app.include_router(webhook_router, tags=["Вебхуки"])


@app.get("/", include_in_schema=False)
async def root():
    """
    Корневой эндпоинт, который перенаправляет на '/docs' (документацию API).
    """
    return RedirectResponse(url='/docs')


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
