from PeaceCard import PeaceCard
from Rulebook import Rulebook
from NotFactionError import NotFactionError
from NotColourError import NotColourError
from ContributionError import ContributionError
from csv import reader

class DebateCard(PeaceCard):

    #stores all debate cards. Temp
    debate_cards = []

    def __init__(self, primary_colour, card_name, level_of_severity, affected_factions):
        """Constructor for DebateCard object. Extends PeaceCard constructor
        
        Arguments:
            primary_colour = string - must be in Rulebook.colours or NotColourError
            card_name = string - should be unique (no checks currently)
            level_of_security = string - must be in Rulebook.colours or NotSeverityError
            affected_factions = dict - key: string - must be in Rulebook.faction or NotFactionError
            value: boolean

        Instance Variables:
            factions_for = set
            factions_against = set
                value: nested dictionary key: string(colour) value: int
            all PeaceCard instance variables
                    
        Dependencies:
            Uses the full init method of its superclass, PeaceCard
            uses Rulebook.colours and Rulebook.factions
        """
        self.factions_for = set()
        self.factions_against = set()
        try:
            for key, value in affected_factions.items():
                if self.real_faction(key) == True:
                    #error raised if failed so not action needed
                    pass
            super().__init__(card_name, level_of_severity, primary_colour)
            #Turn affected_factions dict into two sets, one of factions for and one of factions against
            for key, value in affected_factions.items():
                if value == True:
                    self.factions_for.add(key)
                elif value == False:
                    self.factions_against.add(key)
            self.contributions_against = {}
        except (AttributeError):
            print("The third argument must be of type dict")
        except (NotFactionError):
            print("The key of the input dictionary must be found in Rulebook.factions")
        except (TypeError):
            print("The values of the input dictionary must be of type bool")          
            
    def real_faction(self, faction_check):
        """String as argument. Check if in Rulebook.factions. Return True, else NotFactionError"""
        if faction_check not in Rulebook.factions:
            raise (NotFactionError)
        else:
            return(True)

    def return_faction_impact(self, boolean_string = "true"):
        """Return factions for or against based on input. Return self.colour and severity value.

        Argument:
            boolean_string = string - must be "true" or "false" else raises TypeError
                default value = "true"
        
        Dependencies;
            Call superclass get_impact() method

        Returns
            list - factions_for/against, self.colour and int(severity value)
        """    
        output = []
        if boolean_string == "true":
            output.append(self.factions_against)
        elif boolean_string == "false":
            output.append(self.factions_for)
        else:
            raise(TypeError)
        super_output = self.get_impact()
        for i in super_output:
            output.append(i)
        return (output)
    
    def change_contribution(self, voting_for, voting_player, resource_changed, amount_to_change):
        """Adds a player, colour and amount to contributions_for or contributions_against

        Overrides superclass method
        
        Arguments
            Voting_for = boolean
            voting_player = string
            resource_changed = string 
            amount_to_change = int 
        
        Errors raised:
            NotColourError - if resource_changed not in Rulebook.colours
            TypeError - if amount_to_change is not of type int
            ZeroError - if amount_to_change is 0
            VotingError - if voting_player has voted for and against the card
            ContributionError - if changing the nested value in contributions_for/against
                would result in a negative value
        
        Side Effects:
            Add voting_player if not a key in contributions_for/against
            Add resource_changed if not a key in nested dictionary of contributions_for/against
            Add amount_to_change if no value for nested key in contributions_for/against
            Change value if value for nested key exists
        
        Return:
            dictionary
            Previous value of contributions if vote changed to oppposite
            if not, resource_changed and absolute of amount_to_change if amount_to_change negative
            else empty dictionary
        
        Dependencies:
            Uses inherited method remove_contributions from PeaceCard
            """
        
        #check amount is reasonable
        if type(amount_to_change) != int:
            raise (TypeError)        
        
        #provides refund quantity for resource if needed
        output = {}
        if amount_to_change < 0:
            output = {resource_changed: abs(amount_to_change)}

        #check resource changed is in Rulebook.colours
        if resource_changed not in Rulebook.colours:
            raise (NotColourError)
        
        #check if the player has voted opposite previously. If so remove contributions.
        if voting_player in self.contributions_for:
            if self.contributions_for[voting_player]["for"] != voting_for:
                output = self.remove_contributions(voting_player)

        #assign to instance variable
        if voting_player in self.contributions_for:
            #if key already in child dictionary modify value by amount
            if resource_changed in self.contributions_for[voting_player]:
                self.contributions_for[voting_player][resource_changed] += amount_to_change
                self.contributions_for[voting_player].update({"for": voting_for})
            #if key not present in child dictionary set value to absolute of amount (can't contribute negatively)
            else: 
                self.contributions_for[voting_player].update({resource_changed: amount_to_change})
                self.contributions_for[voting_player].update({"for": voting_for})
        #if key not in parent dictionary make new key value pair using abs amount
        else:
            self.contributions_for.update({voting_player: {resource_changed: amount_to_change}})
            self.contributions_for[voting_player].update({"for": voting_for})
       
        #check contributions haven't made player contribute negative quanitity
        #will have assigned the negative value already, not sure how to fix this
        if self.contributions_for[voting_player][resource_changed] < 0:
            raise (ContributionError)
        
        return(output)
        
    @classmethod
    def make_all_debates(cls, file_path): 
        """Reads all the information from debate cards csv and turns into cards

        Arguments:
            file_path = string - suitable file path else raise PermissionError or FileNotFoundError
        
        Side Effects:
            Card instances stored in the class variable debate_cards.

        Dependencies:
            Uses reader from import csv.
        """
        with open(file_path,"r", newline="") as card_file:
            file_reader = reader(card_file,delimiter=",")
            for line in file_reader:
                #This will exclude headers, empty lines and crisis cards
                if len(line) > 3:
                    #Need to take an uknown number of affected factions and
                    #turn them into a dictionary
                    new_affected_factions = {}
                    for data in line:
                        #format of data in csv is f for for and a for against
                        #followed by the name of the faction
                        #data[0] checks if the first letter is applicable
                        #data[1:] takes the name of the faction from whats left 
                        if data[0] == "f":
                            new_affected_factions.update ({str(data[1:]): True})
                        elif data[0] == "a":
                            new_affected_factions.update ({str(data[1:]): False})
                    new_card = [line[0], line[1], line[2], new_affected_factions]
                    #make a new debate card with the data taken from the line
                    new_debate_card = DebateCard(line[0], line[1], line[2], new_affected_factions)
                    DebateCard.debate_cards.append(new_debate_card)
