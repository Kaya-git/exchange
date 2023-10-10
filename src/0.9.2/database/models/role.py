import enum


class Role(enum.StrEnum):
    User = "user"
    Moderator = "moderator"
    Admin = "admin"
