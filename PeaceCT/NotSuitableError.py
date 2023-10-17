class NotSuitableError(Exception):
    """Raise when a resource colour is attempted to be used for a card which is not applicable"""
    def __init__(self):
        self.message = "Input colour not suitable for card"