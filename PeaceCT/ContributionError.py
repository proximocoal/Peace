class ContributionError(Exception):
    """Raise when a contribution change would result in a negative value"""
    def __init__(self):
        self.message = "Contribution change cannot result in final contribution value being negative."