class StatusCodeNot200(Exception):
    """Rises when the status not equal to code 200."""

    def __init__(self, message, code):
        """__init__ for StatusCodeNot200."""
        super().__init__(message)
        self.code = code
