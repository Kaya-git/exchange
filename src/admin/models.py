from sqladmin import ModelView
from users.models import User
from currencies.models import Currency
from payment_options import PaymentOption
from orders import Order
from service_payment_options import ServicePaymentOption
from reviews import Review
from contacts.models import Contact
from faq.models import FAQ
from enums import Status


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        User.email,
        User.first_name,
        User.second_name,
        User.registered_on,
        User.buy_volume,
        User.role,
    ]
    column_searchable_list = [
        User.email,
        User.first_name,
        User.second_name,
        User.registered_on,
        User.role,
    ]
    can_create = False
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True


class OrderAdmin(ModelView, model=Order):
    name = "Заказ"
    name_plural = "Заказы"
    column_list = [
        Order.id,
        Order.user,
        Order.user_buy_sum,
        Order.buy_currency,
        Order.buy_payment_option,
        Order.user_sell_sum,
        Order.sell_currency,
        Order.sell_payment_option,
        Order.date,
        Order.status,
    ]

    column_details_exclude_list = [
        Order.user_cookie,
        Order.user_id,
        Order.service_sell_po_id,
        Order.service_buy_po_id,
        Order.sell_currency_id,
        Order.buy_currency_id,
        Order.sell_payment_option_id,
        Order.buy_payment_option_id,
    ]
    column_default_sort = [
        (Order.status, Status.Pending),
        (Order.status, Status.Approved),
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class CurrencyAdmin(ModelView, model=Currency):
    name = "Валюта"
    name_plural = "Валюты"
    column_list = [
        Currency.tikker,
        Currency.name,
        Currency.gas,
        Currency.service_margin,
        Currency.reserve,
        Currency.max,
        Currency.min,
        Currency.icon,
    ]
    form_excluded_columns = [
        Currency.service_payment_options, Currency.payment_options
    ]
    column_details_exclude_list = [
        Currency.service_payment_options, Currency.payment_options
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
        PaymentOption.id,
        PaymentOption.banking_type,
        PaymentOption.currency_id,
        PaymentOption.number,
        PaymentOption.holder,
        PaymentOption.is_verified,
        PaymentOption.image,
        # PaymentOption.user_id,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True


class ServicePaymentOptionAdmin(ModelView, model=ServicePaymentOption):
    name = "Сервисный расчетный способ"
    name_plural = "Сервисный способы оплаты"
    column_list = [
        ServicePaymentOption.currency,
        ServicePaymentOption.banking_type,
        ServicePaymentOption.number,
        ServicePaymentOption.holder,
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True


class ReviewAdmin(ModelView, model=Review):
    name = "Отзыв"
    name_plural = "Отзывы"
    column_list = [
        Review.id,
        Review.user_id,
        Review.text,
        Review.data,
        Review.rating
    ]
    can_create = False
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True

class ContactAdmin(ModelView, model=Contact):
    name = "Контакт для связи"
    name_plural = "Контакты для связи"
    column_list = [
        Contact.name,
        Contact.link
    ]
    column_searchable_list = [
        Contact.name
    ]
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True

class FAQAdmin(ModelView, model=FAQ):
    name = "FAQ"
    name_plural = "FAQ"
    column_list = [
        FAQ.question,
        FAQ.answer,
    ]
    column_searchable_list = [
        FAQ.question,
    ]
    can_create = True
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True
