class BaseException(Exception):
    message: str = 'Internal Server Error'

    def __init__(self: 'BaseException', message: str) -> None:
        self.message = message


class ObjectNotFound(BaseException):
    pass


class DatabaseException(BaseException):
    pass


class ProcessesNotFound(BaseException):
    pass
