class NotFactionError(Exception):
    """Raise when a string that is not in Rulebook.factions is input instead of a faction"""
    def __init__(self):
        self.message = "Input was not one of the factions in the Rulebook."