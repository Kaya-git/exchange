import enum


class Status(enum.StrEnum):
    Pending = "pending"
    Timeout = "timeout"
    Canceled = "canceled"
    InProcess = "inprocess"
    Approved = "approved"
    Completed = "completed"
