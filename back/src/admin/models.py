from sqladmin import ModelView

from contacts.models import Contact
from currencies.models import Currency
from enums import Status
from faq.models import FAQ
from orders.models import Order
from payment_options.models import PaymentOption
from pendings.models import PendingAdmin
from reviews.models import Review
from service_payment_options.models import ServicePaymentOption
from users.models import User
from decimal import Decimal


class PendingAdminAdmin(ModelView, model=PendingAdmin):
    name = "Актуальная заявка"
    name_plural = "Актуальные заявки"
    column_list = [
        PendingAdmin.req_act,
        PendingAdmin.order_id,
        PendingAdmin.review_id
    ]
    column_labels = {
        PendingAdmin.id: "ID",
        PendingAdmin.req_act: "Статус",
        PendingAdmin.order_id: "ID ордера",
        PendingAdmin.review_id: "ID отзыва"
    }
    list_template = "custom_list.html"
    can_create = False
    can_delete = True
    can_edit = False
    can_export = False
    can_view_details = True


class UserAdmin(ModelView, model=User):
    name = "Пользователь"
    name_plural = "Пользователи"
    column_list = [
        User.email,
        User.first_name,
        User.second_name,
        User.registered_on,
        User.buy_volume,
        User.sell_volume,
        User.role,
    ]
    column_labels = {
        User.email: "E-mail",
        User.first_name: "Имя",
        User.second_name: "Фамилия",
        User.registered_on: "Дата регистрации",
        User.buy_volume: "Оборот покупок",
        User.sell_volume: "Оборот продаж",
        User.role: "Роль",
        User.payment_options: "ID верификаций",
        User.id: "ID",
        User.is_active: "Статус активации",
        User.is_superuser: "Супер-Пользователь",
        User.is_verified: "Статус верификации"
    }
    column_formatters = {
        User.buy_volume: lambda m, a: format(Decimal(m.buy_volume), "f"),
        User.sell_volume: lambda m, a: format(Decimal(m.sell_volume), "f")
    }
    column_formatters_detail = {
        User.buy_volume: lambda m, a: format(Decimal(m.buy_volume), "f"),
        User.sell_volume: lambda m, a: format(Decimal(m.sell_volume), "f")
    }
    column_details_exclude_list = [
        User.hashed_password
    ]
    column_searchable_list = [
        User.email,
        User.first_name,
        User.second_name,
        User.registered_on,
        User.role,
    ]
    column_sortable_list = [
        User.buy_volume,
        User.sell_volume
    ]
    can_create = False
    can_delete = True
    can_edit = True
    can_export = True
    can_view_details = True


class OrderAdmin(ModelView, model=Order):
    name = "История заказов"
    name_plural = "История заказов"
    column_list = [
        Order.user,
        Order.user_buy_sum,
        Order.buy_currency,
        Order.buy_payment_option,
        Order.user_sell_sum,
        Order.sell_currency,
        Order.sell_payment_option,
        Order.date,
        Order.status,
        Order.transaction_link
    ]
    column_formatters_detail = {
        Order.user_sell_sum: lambda m, a: format(
            Decimal(m.user_sell_sum), "f"
        ),
        Order.user_buy_sum: lambda m, a: format(
            Decimal(m.user_buy_sum), "f"
        )
    }
    column_formatters = {
        Order.user_sell_sum: lambda m, a: format(
            Decimal(m.user_sell_sum), "f"
        ),
        Order.user_buy_sum: lambda m, a: format(
            Decimal(m.user_buy_sum), "f"
        )
    }

    column_labels = {
        Order.id: "ID",
        Order.user: "Пользователь",
        Order.user_buy_sum: "Сумма покупки",
        Order.buy_currency: "Валюта покупки",
        Order.buy_payment_option: "ID способа покупки пользователя",
        Order.user_sell_sum: "Сумма оплаты",
        Order.sell_currency: "Валюта оплаты",
        Order.sell_payment_option: "ID способа оплаты пользователя",
        Order.date: "Дата обмена",
        Order.status: "Статус заявки",
        Order.decline_reason: "Причина отмены",
        Order.transaction_link: "Ссылка на транзакцию"
    }
    column_details_exclude_list = [
        Order.user_cookie,
        Order.user_id,
        Order.service_sell_po_id,
        Order.service_buy_po_id,
        Order.sell_currency_id,
        Order.buy_currency_id,
        Order.sell_payment_option_id,
        Order.buy_payment_option_id,
        Order.pending_admin,
        Order.user_email,
        Order.service_sell_po,
        Order.service_buy_po
    ]
    column_default_sort = [
        (Order.status, Status.верификация_карты),
        (Order.status, Status.ожидание_оплаты),
        (Order.status, Status.проверка_оплаты),
        (Order.status, Status.в_процессе_выплаты),
        (Order.status, Status.исполнена),
        (Order.status, Status.отклонена)
    ]
    column_sortable_list = [
        Order.date,
        Order.status
    ]
    can_create = False
    can_edit = True
    can_delete = True
    can_export = True
    can_view_details = True


class CurrencyAdmin(ModelView, model=Currency):
    name = "Валюта"
    name_plural = "Валюты"
    column_list = [
        Currency.tikker,
        Currency.name,
        Currency.buy_gas,
        Currency.buy_margin,
        Currency.reserve,
        Currency.max,
        Currency.min,
        Currency.icon,
    ]
    column_labels = {
        Currency.id: "ID",
        Currency.type: "Тип валюты",
        Currency.coingecko_tik: "Коингеко тиккер",
        Currency.tikker: "Тиккер валюты",
        Currency.name: "Название валюты",
        Currency.buy_gas: "Комисия за перевод",
        Currency.buy_margin: "Маржинальность в процентах",
        Currency.reserve: "Резервы",
        Currency.max: "Максимум",
        Currency.min: "Минимум",
        Currency.icon: "Иконка"
    }
    form_excluded_columns = [
        Currency.service_payment_options, Currency.payment_options
    ]
    column_details_exclude_list = [
        Currency.service_payment_options, Currency.payment_options
    ]
    column_default_sort = [
        (Currency.tikker, True)
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class PaymentOptionAdmin(ModelView, model=PaymentOption):
    name = "Верификация"
    name_plural = "Верификация"
    column_list = [
        PaymentOption.user,
        PaymentOption.currency,
        PaymentOption.number,
        PaymentOption.holder,
        PaymentOption.is_verified,
        PaymentOption.image,
    ]
    column_labels = {
        PaymentOption.id: "ID",
        PaymentOption.currency: "Валюта",
        PaymentOption.number: "Номер карты/кошелька",
        PaymentOption.holder: "Владелец",
        PaymentOption.is_verified: "Статус верификации",
        PaymentOption.image: "Фото",
        PaymentOption.user: "Пользователь"
    }
    column_details_exclude_list = [
        PaymentOption.user_id,
        PaymentOption.currency_id
    ]
    column_searchable_list = [
        PaymentOption.user,
    ]
    column_sortable_list = [PaymentOption.is_verified]
    can_create = False
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class ServicePaymentOptionAdmin(ModelView, model=ServicePaymentOption):
    name = "Способ оплаты"
    name_plural = "Способы оплаты"
    column_list = [
        ServicePaymentOption.currency,
        ServicePaymentOption.number,
        ServicePaymentOption.holder,
    ]
    column_labels = {
        ServicePaymentOption.currency: "Валюта",
        ServicePaymentOption.number: "Номер карты/кошелька",
        ServicePaymentOption.holder: "Владелец"
    }
    column_details_exclude_list = [
        ServicePaymentOption.currency_id
    ]
    can_create = True
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class ReviewAdmin(ModelView, model=Review):
    name = "Отзыв"
    name_plural = "Отзывы"
    column_list = [
        Review.name,
        Review.text,
        Review.rating
    ]
    column_labels = {
        Review.id: "ID",
        Review.name: "Пользователь",
        Review.text: "Отзыв",
        Review.rating: "Оценка",
        Review.moderated: "Статус модерации"
    }
    column_details_exclude_list = [
        Review.pending_admin
    ]
    can_create = False
    can_edit = True
    can_delete = True
    can_export = False
    can_view_details = True


class ContactAdmin(ModelView, model=Contact):
    name = "Контакт"
    name_plural = "Контакты"
    column_list = [
        Contact.name,
        Contact.link
    ]
    column_labels = {
        Contact.name: "Контакт",
        Contact.link: "Ссылка",
        Contact.id: "ID"
    }
    can_create = True
    can_delete = True
    can_edit = True
    can_export = False
    can_view_details = True


class FAQAdmin(ModelView, model=FAQ):
    name = "FAQ"
    name_plural = "FAQ"
    column_list = [
        FAQ.question,
        FAQ.answer,
    ]
    column_labels = {
        FAQ.question: "Вопрос",
        FAQ.answer: "Ответ",
        FAQ.id: "ID"
    }
    can_create = True
    can_delete = True
    can_edit = True
    can_export = False
    can_view_details = True
