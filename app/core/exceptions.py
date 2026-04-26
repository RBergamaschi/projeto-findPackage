class AppException(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code

class NotFoundException(AppException):
    def __init__(self, message: str = "Not found"):
        super().__init__(message, 404)

class ConflictException(AppException):
    def __init__(self, message: str = "Conflict"):
        super().__init__(message, 409)

class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)

class BadRequestException(AppException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(message, 400)

class ForbiddenException(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)

# Quando colocar o Kafka / Redis

# class ServiceUnavailableException(AppException):
#     def __init__(self, message: str = "Service unavailable"):
#         super().__init__(message, 503)