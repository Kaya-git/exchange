from sqladmin import ModelView
from database.models import User


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
