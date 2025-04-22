class GodorkException(Exception):
    # This exception is used for general errors
    pass

class GodorkTimeout(TimeoutError):
    # This exception is used for timeout errors
    pass

class GodorkMaxRetries(Exception):
    # This exception is used for max retries errors
    pass

class GodorkNoData(Exception):
    # This exception is used for no data errors
    pass