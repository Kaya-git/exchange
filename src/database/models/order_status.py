import enum


class Status(enum.StrEnum):
    Pending = "pending"
    Canceled = "canceled"
    Timeout = "timeout"
    Completed = "completed"


class PendingStatus(enum.IntEnum):
    Canceled = "canceled"
    InProcess = "inprocess"
    Approved = "approved"
