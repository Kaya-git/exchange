from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from starlette.responses import RedirectResponse
from .handlers import authenticate_admin, create_access_token
from users.dependecies import get_current_user
from enums import Role

class AdminAuth(AuthenticationBackend):
    async def login(self,
                    request: Request,
    ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await authenticate_admin(username, password)
        print(user)
        if user:
            acces_token = create_access_token({"sub": str(user.id)})
            print(acces_token)
            request.session.update({"token": acces_token})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        # Usually you'd want to just clear the session
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")
        print(token)
        if not token:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)

        user = await get_current_user(token)
        print(user)
        if not user:
            return RedirectResponse(request.url_for("admin:login"), status_code=302)
        return True

authentication_backend = AdminAuth(secret_key="...")
