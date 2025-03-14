class StatusCodeNot200(Exception):
    """Rises when the status not equal to code 200."""

    message = 'The status code not equal 200'
