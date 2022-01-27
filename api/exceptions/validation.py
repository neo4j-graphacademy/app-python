class ValidationException(Exception):
    def __init__(self, message, details):
        self.message = message
        self.details = details
        super().__init__(self.message)
