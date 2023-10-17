class NotSeverityError(Exception):
    """Raise when a string that is not in Rulebook.severity is input instead of a severity"""
    def __init__(self):
        self.message = "Input was not one of the available severity levels."