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
        PendingOrder.email,
        PendingOrder.get_value,
        PendingOrder.send_value,
        PendingOrder.cc_holder,
        PendingOrder.cc_num,
        PendingOrder.cc_image_name,
        PendingOrder.date
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
        Order.ammount_get,
        Order.get_currency,
        Order.ammount_give,
        Order.give_currency,
        Order.payment_option,
        Order.date,
        Order.status
    ]
    can_create = False
    can_edit = False
    can_delete = False
    can_export = False
    can_view_details = False

    class Metadata:
        name = "История заказа"
        name_plural = "История заказов"
