class GeminiException(Exception):
    def __init__(self, message, original_exception = None):
        super().__init__(message, original_exception)
