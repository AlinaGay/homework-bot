from typing import Optional


class BaseAPIError(Exception):
    """Basic exception for API."""

    @property
    def code(self):
        """."""
        raise NotImplementedError

    @property
    def message(self):
        """."""
        raise NotImplementedError


class CodeMessageMixin:
    """Mixin with code and message for exception."""

    def __init__(
            self,
            code: Optional[str] = None,
            message: Optional[str] = None
    ):
        """."""
        self.code: Optional[str] = code or self.code
        self.message: Optional[str] = message or self.message


class InvalidDataError(CodeMessageMixin, BaseAPIError):
    """Exception for invalid data."""

    code = 'invalid_data'
    message = 'Invalid data'
