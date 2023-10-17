from Rulebook import Rulebook
from NotColourError import NotColourError
from NotSeverityError import NotSeverityError
from NotSuitableError import NotSuitableError
from ZeroError import ZeroError
from csv import reader

class PeaceCard:

    """Represents cards in the game of Peace
    
    Class Variables:
        crisis_cards = list
    
    Instance Variables:
        name = string - should be unique
        contributions_for = dictionary - key: player_name string
            value: nested dictionary. key: string(colour) value: int
        severity = string
        colour = string

    Class Methods:
        make_all_crisis() - makes many crisis cards from csv file
    
    Instance Methods:
        __init__() - constructor method
        __repr__() - uses name variable when used as string
        can_use_resource() - checks if input is acceptable
        get_impact() -returns colour and severity value as dict
        change_contributions_for() -change the instance variable contributions_for
        show_contributions() -show dict for given player in contributions_for
        remove_contributions() - remove all contributions from given player
        make_nested_dict() - returns dict with key of colours and value 0
        set_base_contributions() - fill contributions_for with basic values
        check_all_contributions() - check if player has negative contributions
        check_contribution_change() - check if changing contribution by amount will result in negative
    
    Dependencies:
        reader from csv
        Rulebook.colours, Rulebook.severity, Rulebook.severity_impact
    """

    #For storing all copies of crisis cards. Temp
    crisis_cards = []

    
    def __init__(self, card_name, level_of_severity, primary_colour):
        """ Constructor for PeaceCard object.
    
        Arguments:
            primary_colour = string - must be Rulebook.severity else NotColourError
            level_of_severity = string - must be in Rulebook.severity else NotSeverityError
            name = string
    
        Instance variables: 
            colour = string = primary_colour  
            severity = string = level_of_severity
            name = string = card_name 
            contributions_for = dictionary = empty 

        Dependencies:
            uses Rulebook.colours and Rulebook.severity   
        """
        if primary_colour in Rulebook.colours:
            self.colour = primary_colour
        else:
            raise(NotColourError)
        
        if level_of_severity in Rulebook.severity:
            self.severity = level_of_severity
        else:
            raise(NotSeverityError)
        self.name = card_name
        self.contributions_for = {}
    
    def can_use_resource(self, input_colour):     
        """ Check if a string is in Resource.colours and does not match card colour.

        Argument:
            input_colour = string - must be in Resource.colours or throws NotColourError

        Returns:
            If string matches self.colour returns False
            Else returns True.

        Dependencies:
            Uses Rulebook.colours
        """
        output = True
        if input_colour not in Rulebook.colours:
            raise (NotColourError)
        if input_colour in self.colour:
            output = False
        return (output)
        
    def get_impact(self):
        """Get colour and severity value. Returns colour and int
        
        Dependencies:
            Uses Rulebook.severity_impact
        """
        severity_value = Rulebook.severity_impact[self.severity]
        return(self.colour, severity_value)
        
    def make_nested_dict(self):
        """make the basic dict for nesting in contributions_for
        
        Returns:
            dict with key of colours from Rulebook.colours without self.colour
            value for each key is 0
        
        Dependencies:
            Uses Rulebook.colours
        """
        nested = {}
        for col in Rulebook.colours:
            if col not in self.colour:
                nested.update({col:0})
        return(nested)
    
    def set_base_contributions(self, player_list):
        """input the starting contributions for all players in list.
        
        Arguments:
            player_list = list - list of players in current game
        
        Side Effects:
            changes self.contributions_for to have each item in player_list as keys
            values are nested dictionaries from self.make_nested_dict()
        
        Returns:
            null
        
        Dependencies:
            Uses Rulebook.colours
        """
        nested = self.make_nested_dict()
        for col in Rulebook.colours:
            if col not in self.colour:
                nested.update({col:0})
        for playr in player_list:
            self.contributions_for.update({playr: nested})
    
    def check_all_contributions(self, player_key):
        """Check to see if given player has any contributions less than 1.
        
        Arguments:
            player_key = string
        
        Returns:
            Check the content of self.contributions_for for the player_key
            If they have any contributions less than 0, then return false. Else True
        """
        output = True
        for col in self.contributions_for[player_key]:
            if self.contributions_for[player_key][col] < 0:
                output = False
        return(output)
       
    def check_contribution_change(self, playr, col, change):
        """Check to see if changing a player's contribution is suitable.
        
        Arguments:
            playr = string = should be key in contributions_for.
            col = string = should be in Rulebook.colours
            change = int = proposed change to value of contribution
        
        Returns:
            If the value of contributions_for[playr][col] + change < 0 returns False
            If either key not found returns false
            Else returns True
        """
        output = True
        try:
            if (self.contributions_for[playr][col]) + change < 0:
                output = False
        except (KeyError):
            output = False
        return(output)
            
    def change_contribution(self, input_name, colour_given, amount):
        """Change the value of contributions_for.
        
        Arguments:
            input_name = string - should be key in contributions_for
            colour_given = string - must be in Rulebook.colours or raises NotColourError
            amount = int = must be non 0 int else raises TypeError or ZeroError

        Side Effects:
            changes the value of contributions_for key: input_name
            value = nested dictionary key: colour_given value:amount
        
        Returns:
            If amount not int returns TypeError
            If amount is 0 returns ZeroError
            If input_name not in contributions_for raise KeyError
            If colour_given not in nested dict raise NotColourError
            If contribution change would result in negative value returns False
            If assignment successful returns True

        Dependencies:
            Uses Rulebook.colours, TypeError, KeyError, NotColourError, ZeroError
                self.check_contribution_change
        """
        output = False
        check = True
        if type(amount) != int:
            raise (TypeError)
        if amount == 0:
            raise (ZeroError)
        if input_name not in self.contributions_for:
            raise(KeyError)
        if colour_given not in self.contributions_for[input_name]:
            raise(NotColourError)
        if self.check_contribution_change(input_name, colour_given, amount) is not True:
            check = False
        if check is True:
            self.contributions_for[input_name][colour_given] = amount
            output = True
        return(output)

    def __repr__(self):
        """Return name and class when called to string"""
        return (f"Class: Peace Card. Name: {self.name}")
    
    def show_contributions(self, given_player):
        """Return the value of contributions given by specified player.
        
        Arguments:
        given_player = string - should be player name
        
        Return
        dict corresponding to given_player in self.contributions_for
        if player not in dict raise KeyError
        """
        output = self.contributions_for[given_player]
        return(output)
    
    def remove_contributions(self, given_player):
        """Return the value of contributions given by specified player, then remove them.
        
        Arguments:
        given_player = string - should be player name
        
        Return
        dict corresponding to given_player in self.contributions_for before change
        Raise KeyError if given_player not in self.contributions_for
        
        Side Effects:
        Reassign self.contributions_for[given_player] to an empty dictionary
        """
        output = self.show_contributions(given_player)
        self.contributions_for[given_player] = {}
        return(output)

    @classmethod
    def make_all_crisis(cls, file_path): 
        """Read all information from filepath into card objects

        Arguments:
            file_path = string 
            will raised FileNotFoundError or PermissionError if not suitable file path
        
        Side Effects:
            Store card instances in the class variable crisis_cards.
        
        Dependencies:
            reader from import csv.
        """
        with open(file_path,"r", newline="") as card_file:
            file_reader = reader(card_file,delimiter=",")
            for line in file_reader:
                #bypass headers and blank lines
                if len(line) > 2:
                    new_crisis_card = PeaceCard(line[0], line[1], line[2])
                    PeaceCard.crisis_cards.append(new_crisis_card)     
                    