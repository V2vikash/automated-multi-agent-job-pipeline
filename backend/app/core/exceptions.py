from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger


class BaseAppException(Exception):
    """Base exception for Job Intelligence Platform."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(message)


class ConfigurationError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ServiceUnavailableError(BaseAppException):
    def __init__(self, message: str):
        super().__init__(message, status_code=status.HTTP_530_SITE_IS_FROZEN)


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    Global exception handler catching all uncaught exceptions.
    Logs full exception info internally while returning sanitized error JSON to client.
    """
    logger.error(
        f"Unhandled exception on path {request.url.path}: {str(exc)}",
        exc_info=True,
        extra={"path": str(request.url.path), "method": request.method}
    )

    if isinstance(exc, BaseAppException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": exc.message, "status_code": exc.status_code}
        )

    # Production response: hide stack traces
    if settings.APP_ENV.lower() == "production":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "An internal server error occurred.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
            }
        )

    # Development mode response: show helpful error string
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR
        }
    )
