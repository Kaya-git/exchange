from sqladmin import ModelView
from database.models import User, Commissions, PendingOrder, Order, Currency
from sqladmin.authentication import AuthenticationBackend
from fastapi import Request
from fastapi.responses import RedirectResponse
from typing import Optional


class AdminAuth(AuthenticationBackend):
    async def login(
        self,
        request: Request,
    ) -> bool:
        request.session.update({"token": "..."})
        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(
        self,
        request: Request
    ) -> Optional[RedirectResponse]:
        if "token" not in request.session:
            return RedirectResponse(
                request.url_for("admin:login"),
                status_code=302
                )


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        User.id, User.user_name,
    ]
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True


class CommissionsAdmin(ModelView, model=Commissions):
    name = "Коммиссия"
    name_plural = "Коммиссии"
    column_list = [
        Commissions.gas, Commissions.margin
    ]
    can_create = True
    can_delete = False
    can_edit = True
    can_export = False
    can_view_details = True


class PendingAdmin(ModelView, model=PendingOrder):
    name = "Заказ в работе"
    name_plural = "Заказы в работе"
    column_list = [
        PendingOrder.id,
        PendingOrder.date,
        PendingOrder.email,
        PendingOrder.payment_from,
        PendingOrder.payment_to,
        PendingOrder.status,
        PendingOrder.user_uuid,
    ]
    can_create = False
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class OrdersHistoryAdmin(ModelView, model=Order):
    name = "История заказа"
    name_plural = "История заказов"
    column_list = [
        Order.id,
        Order.user,
        Order.date,
        Order.status,
        Order.payment_from,
        Order.payment_to,
    ]
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False
    can_view_details = False


class CurrencyAdmin(ModelView, model=Currency):
    name = "Валюта"
    name_plural = "Валюты"
    column_list = [
        Currency.id,
        Currency.name,
        Currency.tikker,
        Currency.max,
        Currency.min,
        Currency.reserve
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True
