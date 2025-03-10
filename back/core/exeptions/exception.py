import abc
import typing

import fastapi as fa


class BaseError(abc.ABC, Exception):
    status_code: typing.Optional[int] = None
    default_message: typing.Optional[str] = None

    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message or self.default_message)


class NotFound(BaseError):
    status_code = 404
    default_message = "Not found"


class InternalServerError(BaseError):
    status_code = 500
    default_message = "Internal server error"


class Forbidden(BaseError):
    status_code = 403
    default_message = "Forbidden"


class Unauthorized(BaseError):
    status_code = 401
    default_message = "Unauthorized"


async def api_exception_handler(_, exc: BaseError) -> fa.responses.JSONResponse:
    return fa.responses.JSONResponse(
        status_code=exc.status_code, content={"message": exc.message}
    )


exeption_handlers: dict[typing.Type[Exception], typing.Callable] = {
    BaseError: api_exception_handler
}
