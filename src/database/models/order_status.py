import enum


class Status(enum.IntEnum):
    Pending = 0
    Canceled = 1
    Timeout = 2
    Completed = 3
