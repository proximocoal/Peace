class PlayerNameError(Exception):
    """Raise when a player is made with a name that matches another player's name"""
    def __init__(self):
        self.message = "Your given player name has already been used, you must use something unique."