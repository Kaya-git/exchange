from sqladmin import ModelView
from database.models import (
    User, Commissions,
    PendingOrder, Currency,
    PaymentOption, CompletedOrder,
)
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
    column_searchable_list = [
        User.id,
        User.user_name,
        User.role,
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
        PendingOrder.email,
        PendingOrder.give_amount,
        PendingOrder.give_currency_id,
        PendingOrder.get_amount,
        PendingOrder.get_currency_id,
        PendingOrder.date,
        PendingOrder.status,
        PendingOrder.user_uuid,
    ]

    can_create = False
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class OrdersHistoryAdmin(ModelView, model=CompletedOrder):
    name = "История заказа"
    name_plural = "История заказов"
    column_list = [
        CompletedOrder.id,
        CompletedOrder.user_id,
        CompletedOrder.date,
        CompletedOrder.status,
        CompletedOrder.give_amount,
        CompletedOrder.give_currency,
        CompletedOrder.get_amount,
        CompletedOrder.get_currency,
        CompletedOrder.payment_options,
    ]
    column_searchable_list = [
        CompletedOrder.user_id,
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
        Currency.tikker_id,
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


class PaymentOptionAdmin(ModelView, model=PaymentOption):
    name = "Расчетный способ"
    name_plural = "Способы оплаты"
    column_list = [
        PaymentOption.cc_num_x_wallet,
        PaymentOption.cc_holder,
        PaymentOption.image_name,
        PaymentOption.payment_point,
        PaymentOption.clien_service_belonging,
        PaymentOption.currency_id,
        PaymentOption.pending_order_id,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True
