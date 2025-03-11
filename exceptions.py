class InvalidDataError(Exception):
    """Exception raised when the provided data is invalid."""

    code = 'invalid_data'
    message = 'Invalid data'


class StatusCodeNot200(Exception):
    """Exception raised when the status"""
    """of response to API not equal to code 200."""

    def __init__(self, message, code):
        """__init__ for StatusCodeNot200."""
        super().__init__(message)
        self.code = code
