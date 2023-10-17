class FactionUsedError(Exception):
    """Raise when a faction is assigned to a player when the faction is already assigned to another player"""
    def __init__(self):
        self.message = "You have chosen a faction that has already been taken. Only one player can use each faction"