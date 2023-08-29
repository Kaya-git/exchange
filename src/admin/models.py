from sqladmin import ModelView
from database.models import User, Commissions, PendingOrder, Order


class UserAdmin(ModelView, model=User):
    column_list = [
        User.id, User.user_name,
    ]
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True

    class Metadata:
        name = "Пользователь"
        name_plural = "Пользователи"


class CommissionsAdmin(ModelView, model=Commissions):
    column_list = [
        Commissions.gas, Commissions.margin
    ]
    can_create = False
    can_delete = False
    can_edit = True
    can_export = False
    can_view_details = True

    class Metadata:
        name = "Коммиссия"
        name_plural = "Коммиссии"


class PendingAdmin(ModelView, model=PendingOrder):
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
    can_edit = False
    can_delete = True
    can_export = False
    can_view_details = True

    class Metadata:
        name = "Заказ в работе"
        name_plural = "Заказы в работе"


class OrdersHistoryAdmin(ModelView, model=Order):
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

    class Metadata:
        name = "История заказа"
        name_plural = "История заказов"
