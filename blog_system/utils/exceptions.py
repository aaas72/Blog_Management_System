class AppError(Exception):
    def __init__(self, message: str, code: str, status_code: int):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)

class NotFoundError(AppError):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, "NOT_FOUND", 404)

class ValidationError(AppError):
    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, "VALIDATION_ERROR", 400)

class AuthError(AppError):
    def __init__(self, message: str = "Authentication failed", status_code: int = 401):
        super().__init__(message, "AUTH_ERROR", status_code)

class ForbiddenError(AppError):
    def __init__(self, message: str = "Access forbidden"):
        super().__init__(message, "FORBIDDEN", 403)
