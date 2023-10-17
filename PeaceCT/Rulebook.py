from NotFactionError import NotFactionError
from NotColourError import NotColourError
from NotSeverityError import NotSeverityError

class Rulebook():

    """Contains variables for use by multiple classes.

    In future would like to be able to generate instances so people can
    modify the rules themselves, but at the moment just has class variables
    and a __repr__ class method so it displays its variables.

    Class Variables:
    factions - Set - countries that the players can control
    colours - Set - Used for player resource colours. Also used by cards
    base_resources - int - divide by the # of players to get starting resources
    severity - Set - Used for checking the names of severity on cards
    severity_impact - Dictionary - check the effect of severity.

    Class Methods:
    is_faction - returns boolean or error if arg is in factions
    is_colour - returns boolean or error if arg is in colours
    is_severity - returns boolean or error if arg is in severity
    __repr__ - return string of all class variables
    """

    factions = {"US", "UK", "France", "Italy", "Japan", "Canada", "Romania"}
    colours = {"red", "yellow", "blue"}
    base_resources = 25
    severity = {"critical", "high", "moderate"}
    severity_impact = {"critical": 3, "high": 2, "moderate": 1}

    def __init__(self):
        """Placeholder constructor method."""
        pass

    @classmethod
    def __repr__(cls):
        """Overwrite __repr__ to include variables"""
        return (f"""
        factions: {Rulebook.factions}
        colours: {Rulebook.colours}
        base_resources: {Rulebook.base_resources}
        severity: {Rulebook.severity}
        severity_impact: {Rulebook.severity_impact}
        """)

    @classmethod
    def is_faction(cls, given_faction):
        """Check string argument is in factions else raise NotFactionError"""
        output = True
        if given_faction not in Rulebook.factions:
            raise NotFactionError
        return output
    
    @classmethod
    def is_colour(cls, given_colour):
        """Check string argument is in colours else raise NotColourError"""
        output = True
        if given_colour not in Rulebook.colours:
            raise NotColourError
        return output
    
    @classmethod
    def is_severity(cls, given_severity):
        """Check string argument is in severity else raise NotSeverityError"""
        output = True
        if given_severity not in Rulebook.severity:
            raise NotSeverityError
        return output
