from typing import Optional


class BaseAPIError(Exception):
    """."""

    @property
    def code(self):
        """."""
        raise NotImplementedError

    @property
    def message(self):
        """."""
        raise NotImplementedError


class CodeMessageMixin:
    """."""

    def __init__(
            self,
            code: Optional[str] = None,
            message: Optional[str] = None
    ):
        """."""
        self.code: Optional[str] = code or self.code
        self.message: Optional[str] = message or self.message


class InvalidDataError(CodeMessageMixin, BaseAPIError):
    """."""

    code = 'invalid_data'
    message = 'Invalid data'
