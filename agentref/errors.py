from typing import Optional


class AgentRefError(Exception):
    code: str
    status: int
    request_id: str

    def __init__(self, message: str, code: str, status: int, request_id: str) -> None:
        super().__init__(message)
        self.code = code
        self.status = status
        self.request_id = request_id


class AuthError(AgentRefError):
    def __init__(self, message: str, code: str, request_id: str) -> None:
        super().__init__(message, code, 401, request_id)


class ForbiddenError(AgentRefError):
    """403 — authenticated but not authorized: wrong scope, ownerType, or trust level."""

    def __init__(self, message: str, code: str, request_id: str) -> None:
        super().__init__(message, code, 403, request_id)


class ValidationError(AgentRefError):
    details: Optional[object]

    def __init__(
        self,
        message: str,
        code: str,
        request_id: str,
        details: Optional[object] = None,
    ) -> None:
        super().__init__(message, code, 400, request_id)
        self.details = details


class NotFoundError(AgentRefError):
    def __init__(self, message: str, code: str, request_id: str) -> None:
        super().__init__(message, code, 404, request_id)


class ConflictError(AgentRefError):
    def __init__(self, message: str, code: str, request_id: str) -> None:
        super().__init__(message, code, 409, request_id)


class RateLimitError(AgentRefError):
    retry_after: int

    def __init__(self, message: str, code: str, request_id: str, retry_after: int) -> None:
        super().__init__(message, code, 429, request_id)
        self.retry_after = retry_after


class ServerError(AgentRefError):
    def __init__(self, message: str, code: str, status: int, request_id: str) -> None:
        super().__init__(message, code, status, request_id)
