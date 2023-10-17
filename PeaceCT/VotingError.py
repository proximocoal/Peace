class VotingError(Exception):
    """Raise when a player would vote on a debate card but has already voted oppposite"""
    def __init__(self):
        self.message = "Cannot vote both for and against a motion"