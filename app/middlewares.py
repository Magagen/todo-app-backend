import logging
from time import perf_counter

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logging import configure_logging

configure_logging()
logger = logging.getLogger("app.middleware")


class RequestCounterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app):
        super().__init__(app)
        self.counter: int = 0

    async def dispatch(self, request: Request, call_next) -> Response:
        started_at = perf_counter()
        try:
            response: Response = await call_next(request)  # Работа самого эндпоинта
            response.headers["X-Request-Number"] = str(self.counter)
            self.counter += 1
        except Exception:
            duration_ms = (perf_counter() - started_at) * 1000
            logger.exception(
                "Request failed: %s %s completed_in=%.2fms",
                request.method,
                request.url.path,
                duration_ms,
            )
            raise

        duration_ms = (perf_counter() - started_at) * 1000
        logger.info(
            "%s %s -> %s (%.2f ms)",
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
