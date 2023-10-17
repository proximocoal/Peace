class NotColourError(Exception):
    """Raise when a string that is not in Rulebook.colours is input instead of a colour"""
    def __init__(self):
        self.message = "Input was not one of the available colours."