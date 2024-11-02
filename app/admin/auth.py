from fastapi.requests import Request
from sqladmin.authentication import AuthenticationBackend

from app.config import settings
from app.users.dao import UserDAO
from fastapi_users.password import PasswordHash, PasswordHelper
from passlib.context import CryptContext

class AdminAuth(AuthenticationBackend):
    """Класс для аутентификации пользователей с возможностью администрирования."""

    async def login(self, request: Request) -> bool:
        """Показывает форму для входа в админку."""
        form = await request.form()
        username, password = form['username'], form["password"]

        user = await UserDAO.get_object(username=username)

        if user and user.is_verified and user.is_superuser:
            request.session.update({'token': '...'})
        return True

    async def logout(self, request: Request) -> bool:
        """Закрывает админ-сессию."""
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        """Проверяет доступность возможностей администрирования."""
        token = request.session.get('token')

        if not token:
            return False
        return True


authentication_backend = AdminAuth(secret_key=settings.PASSWORD)
