class ZeroError(Exception):
    """Raise when 0 is input when the integer must be at least 1"""
    def __init__(self):
        self.message = "Input must be a non-zero integer value."