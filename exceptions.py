from typing import Optional


class BaseAPIError(Exception):
    """Basic exception for API."""

    @property
    def code(self):
        """A code describing the code of the error."""
        raise NotImplementedError

    @property
    def message(self):
        """A message describing the reason for the error."""
        raise NotImplementedError


class CodeMessageMixin:
    """Mixin with code and message for exception."""

    def __init__(
            self,
            code: Optional[str] = None,
            message: Optional[str] = None
    ):
        """
        A code describing the code of the error.
        A message describing the reason for the error.
        """
        self.code: Optional[str] = code or self.code
        self.message: Optional[str] = message or self.message


class InvalidDataError(CodeMessageMixin, BaseAPIError):
    """Exception raised when the provided data is invalid."""

    code = 'invalid_data'
    message = 'Invalid data'
