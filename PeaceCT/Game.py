import ZeroError
import Player
import FactionUsedError
import PlayerNameError
import Rulebook
import NotFactionError
import NotValidCardError
import NotColourError
import NotSuitableError
import ContributionError

class Game:

    """Represents the particular gaming session that players would be involved in. 
    """

    def __init__(self, given_rounds, dict_of_players):

        """Constructor for class Game objects.

        Arguments
            First argument must be a non-zero integer.
            Second argument must be a dictionary.
            Second argument keys must be unique factions in Rulebook.factions
            Second argument values must be unique strings.
        
        Instance Variables:
            total_rounds = int = value of first argument
            set_of_players = set = Players made within initiatlisation
            factions_used = set = values of second argument
            current_round = int = 0
            cards_in_play = tuple = empty
            cards_used = set = empty
            player_turn = Player = empty

        Dependencies:
            Player Class
            Rulebook.factions
        """
        #check given_rounds is an int and that the game won't end immediately otherwise assign
        try:
            if type(given_rounds) != int:
                raise (TypeError)
            if given_rounds > 0:
                self.total_rounds = given_rounds
            else:
                raise(ZeroError)
        except(TypeError):
            print("given_rounds must be of type int.")
        except(ZeroError):
            print(ZeroError.message)
        
        #iterate through the dict to make sure player and faction are reasonable and assign
        self.set_of_players = set()
        self.factions_used = set()
        try:
            for key, value in dict_of_players.items():
                if self.player_available(value) and self.faction_available(key):
                    new_player = Player(key, value)
                    self.set_of_players.add(new_player)
                    self.factions_used.add(value)
        except (FactionUsedError):
            print(FactionUsedError.message)
        except (PlayerNameError):
            print(PlayerNameError.message)        
        except(AttributeError):
            print("Entered dict_of_players was not of type dict.")

        self.current_round = 0
        self.cards_in_play = ()
        self.cards_used = set()
        self.player_turn = ""
        
    
    def player_available(self, given_string):
        """Make sure there are no players with the same name.

        string as an argument. 
        If no player has the same name return True, else raise PlayerNameError.
        """
        if given_string in self.set_of_players:
                raise(PlayerNameError)
        else:
            return(True)
    
   
    def faction_available(self, country):
        """Make sure argument is a faction and not in self.faction_used.

        Arguments:
            string as an argument.
            
        Errors:
            Check string is in Rulebook.factions. Else NotFactionError
            Check string is not in self.faction_used. Else FactionUsedError
        
        Return:
            Return True if complete

        Dependencies:
            Rulebook.factions
        """
        if country not in Rulebook.factions:
            raise(NotFactionError)
        else:
            if country in self.factions_used:
                raise(FactionUsedError)
        return(True)
    
    
    def increment_round(self):
        """Moves the game from one round to the next.
        
        Side Effects:
            Increase instance variable round_number by one. 
            call new_debate_cards() changing cards_in_play
            move old cards_in_play to cards_used

        Returns:    
            Return False if round_number greater than total_round, else True.
        """
        self.current_round += 1
        output = True
        #check for game end
        if self.current_round > self.total_rounds:
            output = False
        #otherwise reset the game cards
        else:
            for card in self.cards_in_play:
                self.cards_used.add(card)
            self.new_debate_cards()
        return(output)

    def assign_starting_resources(self):
        """Assign starting resources to players.
     
        Side Effects:
            Change value of resources for Player objects in set_of_players
        
        Returns:
            Returns True if assignment successfull, else returns False
        
        Dependencies:
            Player Class
            Rulebook.colours
        """    

        divisor = len(self.set_of_players)
        assign = Rulebook.base_resources // divisor
        output = True
        
        for reg_player in self.set_of_players:
            for colour in Rulebook.colours:
                output = reg_player.increment_resource(colour, assign)
                if output == False:
                    break
        return (output)
    
    """Initiates the game. 
    
    Arguments:
        None

    Returns:
        Return False if there are no players in list_of_players.
        Else True
    
    Side Effects:
        Assign current round to 1
        Assign first player to the first player in the list_of_players.
        Assign new cards_in_play and assign starting resources to the players.
    """
    def start_game(self):
        check = True
        if len(self.set_of_players) < 1:
            check = False
        else:
            self.player_turn = self.set_of_players[0]
            self.current_round = 1
            self.cards_in_play = self.new_debate_cards()
            self.assign_starting_resources()
        return(check)
    

    def make_debate_contribution(self, voting_player, target_card, voting_for, resource_used, amount = 1):
        """
        ############################################################################################
        #This was me trying to make a massive method to handle all votes for all types of cards
        #I think it makes sense to start simpler and call on the simpler methods in the more complicated ones.
        #TEMP
        """
        #Separate try blocks to avoid multiple errors of the same type
        output = ""
        try:
            if target_card not in self.cards_in_play:
                raise(NotValidCardError)
            if type(voting_for) != bool:
                raise (TypeError)
            if resource_used not in Rulebook.colours:
                raise (NotColourError)
        except (NotValidCardError):
            output = NotValidCardError.message
        except (TypeError):
            output = "argument voting-for must be of type boolean"
        except (NotColourError):
            output = "resources_used must be in Rulebook.colours"
        except (Exception):
            output = "Something unexpected occured checking input arguments"
        else:
            try:
                resource_legal = target_card.can_use_resource(resource_used)
                vote_legal = voting_player.check_resource(resource_used, amount)
                if vote_legal and resource_legal:
                    voting_player.increment_resource((-resource_used),amount)
                    target_card.change_contribution(voting_for, voting_player, resource_used, amount)
            except (ZeroError):
                output = "resources_used value must not be less than 1"
            except (TypeError):
                output = "resources_used value must be of type int."
            except (NotColourError):
                output = "Key of resources_used must be a colour in Rulebook.colours."
            except (NotSuitableError):
                output = "Key of resources_used matched target card colour."
            except (ContributionError):
                output = ContributionError.message
            except (Exception):
                output = "Something unexpected happened"
        #checking the value of voting_for rather than just using its value is unnecessary
        #But I think makes the code more readable.
        if len(output) == 0:
            return(f"Voting player: {voting_player} successfully contributed to {target_card.name}")
