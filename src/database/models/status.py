import enum


class Status(enum.StrEnum):
    Pending = "pending"
    Timeout = "timeout"
    Canceled = "canceled"
    Inprocces = "inprocces"
    Approved = "approved"
    Completed = "completed"
