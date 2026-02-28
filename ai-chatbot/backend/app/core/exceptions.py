from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class AuthenticationError(Exception):
    def __init__(self, detail: str = "Authentication failed"):
        self.detail = detail


class ModelUnavailableError(Exception):
    def __init__(self, detail: str = "Model is unavailable"):
        self.detail = detail


class FileProcessingError(Exception):
    def __init__(self, detail: str = "File processing failed"):
        self.detail = detail


class RateLimitError(Exception):
    def __init__(self, detail: str = "Rate limit exceeded"):
        self.detail = detail


def register_exception_handlers(app):
    @app.exception_handler(AuthenticationError)
    async def auth_error_handler(request: Request, exc: AuthenticationError):
        return JSONResponse(status_code=401, content={"detail": exc.detail})

    @app.exception_handler(ModelUnavailableError)
    async def model_error_handler(request: Request, exc: ModelUnavailableError):
        return JSONResponse(status_code=503, content={"detail": exc.detail})

    @app.exception_handler(FileProcessingError)
    async def file_error_handler(request: Request, exc: FileProcessingError):
        return JSONResponse(status_code=422, content={"detail": exc.detail})

    @app.exception_handler(RateLimitError)
    async def rate_limit_handler(request: Request, exc: RateLimitError):
        return JSONResponse(status_code=429, content={"detail": exc.detail})
