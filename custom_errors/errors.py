from loguru import logger
from pydantic import BaseModel


class MyError(Exception):
    def __init__(self, message: str = ""):
        self.message = message
        super().__init__(message)


class UnexpectedError(MyError):
    pass


class InternalServerError(MyError):
    pass


class ExternalAPIError(MyError):
    pass


class BadRequestError(MyError):
    pass


class NotFoundError(MyError):
    pass


class PermissionDeniedError(MyError):
    pass


class AlreadyExistsError(MyError):
    pass


class LogicError(MyError):
    pass


class ErrorDTO(BaseModel):
    code: int
    type: str
    message: str

    @classmethod
    def factory(cls, error: Exception) -> "ErrorDTO":
        code: dict = {
            InternalServerError: 500,
            BadRequestError: 400,
            NotFoundError: 404,
            PermissionDeniedError: 403,
            AlreadyExistsError: 409,
            LogicError: 400,
            ExternalAPIError: 400,
        }
        if issubclass(error.__class__, MyError):
            return ErrorDTO(
                code=code[error.__class__],
                type=error.__class__.__name__,
                message=error.message  # noqa
            )
        logger.error(f'{error.__class__.__name__}: {error}')
        return ErrorDTO(code=418, type=error.__class__.__name__, message=str(error))

    def __bool__(self):
        return False


__all__ = [
    "MyError",
    "ErrorDTO",
    "UnexpectedError",
    "InternalServerError",
    "BadRequestError",
    "NotFoundError",
    "PermissionDeniedError",
    "AlreadyExistsError",
    "LogicError",
    "ExternalAPIError",
]
