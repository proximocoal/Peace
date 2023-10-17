class NotValidCardError(Exception):
    """Raise when a card cannot be found in an active game."""
    def __init__(self):
        self.message = "Target card not in play"