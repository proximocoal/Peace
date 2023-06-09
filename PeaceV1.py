from csv import reader as reader


class FactionUsedError(Exception):
    """Raise when a faction assigned to a player that is already assigned"""
    def __init__(self):
        self.message = "You have chosen a faction that has already been taken.\
        Only one player can use each faction"


class PlayerNameError(Exception):
    """Raise when player made with a name that matches another player's name"""
    def __init__(self):
        self.message = "The player name has already been used."


class NotColourError(Exception):
    """Raise when a string in Rulebook.colours expected and not given."""
    def __init__(self):
        self.message = "Input was not one of the available colours."


class NotSeverityError(Exception):
    """Raise when a string in Rulebook.severity is expected and not given"""
    def __init__(self):
        self.message = "Input was not one of the available severity levels."


class NotFactionError(Exception):
    """Raise when a string in Rulebook.factions is expected and not given."""
    def __init__(self):
        self.message = "Input was not one of the factions in the Rulebook."


class ZeroError(Exception):
    """Raise when 0 is input when the integer must be at least 1"""
    def __init__(self):
        self.message = "Input must be a non-zero integer value."


class NotSuitableError(Exception):
    """Raise when a colour given is not applicable to a card"""
    def __init__(self):
        self.message = "Input colour not suitable for card"


class VotingError(Exception):
    """Raise when a player votes both for and against a debate """
    def __init__(self):
        self.message = "Cannot vote both for and against a motion"


class NotValidCard(Exception):
    """Raise when a card cannot be found in an active game."""
    def __init__(self):
        self.message = "Target card not in play"


class ContributionError(Exception):
    """Raise when a contribution change would result in a negative value"""
    def __init__(self):
        self.message = "Contribution cannot be negative."


class Rulebook():

    """Contains variables for use by multiple classes.

    In future would like to be able to generate instances so people can
    modify the rules themselves, but at the moment just has class variables
    and a __repr__ class method so it displays its variables.

    Class Variables:
        factions - Set - countries that the players can control
        colours - Set - Used for player resource colours. Also used by cards
        base_resources - int - used to get starting resources
        severity - Set - Used for checking the names of severity on cards
        severity_impact - Dictionary - check the effect of severity.
    """

    factions = {"USA", "UK", "France", "Italy", "Japan", "Canada", "Romania"}
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
               severity_impact: {Rulebook.severity_impact})
               """)


class Player:
    """Represents the human players who take part in the game.

    Instance Variables:
        self.resources - dictionary - the currency players can use in game
        self.user_faction - string - the country the player controls
        self.player_name - string - name of the player

    Instance methods:
        __init__() - constructor for the class
        __repr__() - overwrites to give instance variables
        increment_resources() - change the resources of the player
        check_loss() - see if the player has less than 1 of any resource

    Dependencies:
        Rulebook.factions
    """

    def __init__(self, faction_choice, name_given):
        """Constructor for instances of class Player

        Arguments:
            faction_choice - string - must be present in Rulebook.factions
            name_given - string - should be unique among other players

        Instance Variables:
            player_name = string = name_given
            user_faction = string = faction_choice
            resources = dictionary = {"red": 0, "yellow": 0, "blue": 0}

        Dependencies:
            Rulebook.factions
        """

        if faction_choice in Rulebook.factions:
            self.user_faction = faction_choice
        else:
            raise (NotFactionError)
        self.player_name = name_given
        self.resources = {"red": 0, "yellow": 0, "blue": 0}

    def __repr__(self):
        """Return player_name and name of class when called as string"""
        return (f"Class: Player, name: {self.player_name}")

    def increment_resource(self, input_colour, amount):
        """Change the values of self.resources by quantity of amount.

        Arguments:
            input_colour - string - should be key in resources
            amount - int - with accompanying signage (e.g. -)

        Side Effects:
            resources - key input_colour changed by amount

        Return:
            new value of changed resource
        """
        self.resources[input_colour] += amount
        return (self.resources[input_colour])

    def check_loss(self):
        """check if any values in resources are less than 1. Return boolean."""
        output = False
        for value in self.resources.values():
            if value < 1:
                output = True
                break
        return (output)

    def check_resource(self, resource, quantity):
        """Check player has resource greater or equal to quanitity.

        Arguments:
            resource = string
            quantity = int

        Returns:
            TypeError if quanitity not type int
            ZeroError if quantity less than 1
            Else Boolean
        """
        if type(quantity) != int:
            raise (TypeError)
        if quantity < 1:
            raise (ZeroError)
        output = True
        if self.resources[resource] < quantity:
            output = False
        return (output)


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
        change_contributions_for() -change contributions_for
        show_contributions() -show dict for given player in contributions_for
        remove_contributions() - remove all contributions from given player

    Dependencies:
        reader from csv
        Rulebook.colours, Rulebook.severity, Rulebook.severity_impact
    """

    # For storing all copies of crisis cards. Temp
    crisis_cards = []

    def __init__(self, card_name, level_of_severity, primary_colour):
        """ Constructor for PeaceCard object.

        Arguments:
            primary_colour = string
            level_of_severity = string
            name = string

        Instance variables:
            colour = string = primary_colour
            severity = string = level_of_severity
            name = string = card_name
            contributions_for = dictionary = empty

        Dependencies:
            uses Rulebook.colours and Rulebook.severity

        Returns:
            NotColourError if primary_colour not in Rulebook.colours
            NotSeverityError if level_of_severity not in Rulebook.severity
        """
        try:
            if primary_colour in Rulebook.colours:
                self.colour = primary_colour
            else:
                raise (NotColourError)

            if level_of_severity in Rulebook.severity:
                self.severity = level_of_severity
            else:
                raise (NotSeverityError)
        except (NotColourError):
            print(NotColourError.message)
        except (NotSeverityError):
            print(NotSeverityError.message)
        self.name = card_name
        self.contributions_for = {}

    def can_use_resource(self, input_colour):
        """ Check if string in Resource.colours and not self.colour.

        Argument:
            input_colour = string

        Returns:
            NotColourError if input_colour not in Rulebook.colours
            NotSuitableError if string matches self.colour
            Else returns True.

        Dependencies:
            Uses Rulebook.colours
        """
        if input_colour not in Rulebook.colours:
            raise (NotColourError)
        if input_colour not in self.colour:
            raise (NotSuitableError)
        return (True)

    def get_impact(self):
        """Get colour and severity value. Returns tuple

        Dependencies:
            Uses Rulebook.severity_impact
        """
        severity_value = Rulebook.severity_impact[self.severity]
        output = (self.colour, severity_value)
        return (output)

    def change_contribution(self, input_name, colour_given, amount):
        """Change the value of contributions_for.

        Arguments:
            input_name = string - should match player name
            colour_given = string
            amount = int

        Side Effects:
            changes the value of contributions for to key: input_name
            value = nested dictionary key: colour_given value:amount

        Returns:
            NotColourError if colour_given not in Rulebook.colours
            TypeError if amount not of type int
            ZeroError if amount value is 0
            NotSuitableError if colour_given matches self card colour
            if assignment successful returns True, else False

        Temp:
            Currently handles raised exceptions

        Dependencies:
            Uses Rulebook.colours
        """
        try:
            output = False
            if type(amount) != int:
                raise (TypeError)
            if amount == 0:
                raise (ZeroError)
            if colour_given not in Rulebook:
                raise (NotColourError)
            if self.can_use_resource(colour_given):
                new_entry = {colour_given: amount}
                self.contributions_for[input_name].append(new_entry)
                output = True
        except (TypeError, ZeroError):
            print("amount must be a non-zero integer")
        except (NotColourError):
            print(NotColourError.message)
        except (NotSuitableError):
            print(NotSuitableError.message)
        finally:
            return (output)

    def __repr__(self):
        """Return name and class when called to string"""
        return (f"Class: Peace Card. Name: {self.name}")

    def show_contributions(self, given_player):
        """Return the value of contributions given by specified player.

        Arguments:
        given_player = string - should be player name

        Return
        dict corresponding to given_player in self.contributions_for"""
        output = {}
        if given_player in self.contributions_for:
            for key, value in self.contributions_for[given_player]:
                output.update({key: value})
        return (output)

    def remove_contributions(self, given_player):
        """Return value of contributions given by player, then remove.

        Arguments:
        given_player = string - should be player name

        Return
        dict corresponding to given_player in self.contributions_for

        Side Effects:
        Reassign self.contributions_for[given_player] to an empty dictionary
        """
        output = self.show_contributions(given_player)
        self.contributions_for[given_player] = {}
        return (output)

    @classmethod
    def make_all_crisis(cls, file_path):
        """Read all information from filepath into card objects

        Arguments:
            file_path = string

        Side Effects:
            Store card instances in the class variable crisis_cards.

        Dependencies:
            reader from import csv.

        Return:
            FileNotFoundError if can not file_path file
            PermissionError if filepath leads to disallowed area
            Else None
        """
        with open(file_path, "r", newline="") as card_file:
            file_reader = reader(card_file, delimiter=",")
            for line in file_reader:
                # bypass headers and blank lines
                if len(line) > 2:
                    new_crisis_card = PeaceCard(line[0], line[1], line[2])
                    PeaceCard.crisis_cards.append(new_crisis_card)


class DebateCard(PeaceCard):

    # stores all debate cards. Temp
    debate_cards = []

    def __init__(self, primary_colour, card_name, severity_lvl, aff_factions):
        """Constructor for DebateCard object. Extends PeaceCard constructor

        Arguments:
            primary_colour = string
            card_name = string - should be unique (no checks currently)
            severity_lvl = string
            aff_factions = dictionary -
                key: string - value: boolean

        Instance Variables:
            factions_for = set
            factions_against = set
                value: nested dictionary key: string(colour) value: int
            all PeaceCard instance variables

        Dependencies:
            Uses the full init method of its superclass, PeaceCard
            uses Rulebook.colours, Rulebook.factions and Rulebook.severity

        Returns:
            NotColourError if primary_colour not in Rulebook.colours
            NotSeverityError if severity_lvl not in Rulebook.severity
            NotFactionError if nested dict key not in Rulebook.factions
        """
        self.factions_for = set()
        self.factions_against = set()
        try:
            for key, value in aff_factions.items():
                if self.real_faction(key) is True:
                    # error raised if failed so not action needed
                    pass
            super().__init__(primary_colour, card_name, severity_lvl)
            # Turn affected_factions dict into two sets
            for key, value in aff_factions.items():
                if value is True:
                    self.factions_for.add(key)
                elif value is False:
                    self.factions_against.add(key)
            self.contributions_against = {}
        except (AttributeError):
            print("The third argument must be of type dict")
        except (NotFactionError):
            print("Key of dictionary must be found in Rulebook.factions")
        except (TypeError):
            print("The values of the input dictionary must be of type bool")

    def real_faction(self, faction_check):
        """Check if faction_check in Rulebook.factions."""
        if faction_check not in Rulebook.factions:
            raise (NotFactionError)
        else:
            return (True)

    def motion_passed(self, boolean_string="true"):
        """Return factions for/against, self.colour and severity value.

        Argument:
            boolean_string = string
                default value = "true"

        Dependencies:
            Call superclass get_impact() method

        Returns:
            TypeError if boolean_strong not "True" or "False"
            set - factions_for/against, self.colour and int(severity value)
        """
        output = set()
        if boolean_string == "true":
            output.add(self.factions_against)
        elif boolean_string == "false":
            output.add(self.factions_for)
        else:
            raise (TypeError)
        super_output = self.get_impact()
        for i in super_output:
            output.add(i)
        return (output)

    def change_contribution(self, v_for, v_player, resource_changed, amount):
        """Adds a player, colour and amount relevant instance variable.

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
            ContributionError - if player contribution is negative

        Side Effects:
            Add player if not a key in contributions_for/against
            Add resource if not in nested dictionary of variable
            Add amount if no value for nested key in variable
            Change value if value for nested key exists

        Return:
            dictionary
            Previous value of contributions if vote changed to oppposite
            if not, resource_changed and absolute of amount_to_change
            else empty dictionary

        Dependencies:
            Uses inherited method remove_contributions from PeaceCard
            """

        # check amount is reasonable
        if type(amount) != int:
            raise (TypeError)

        # provides refund quantity for resource if needed
        output = {}
        if amount < 0:
            output = {resource_changed: abs(amount)}

        # check resource changed is in Rulebook.colours
        if resource_changed not in Rulebook.colours:
            raise (NotColourError)

        # check if player has voted opposite previously.
        # If so remove contributions.
        if v_player in self.contributions_for:
            if self.contributions_for[v_player]["for"] != v_for:
                output = self.remove_contributions(v_player)

        # assign to instance variable
        if v_player in self.contributions_for:
            # if key already in child dictionary modify value by amount
            if resource_changed in self.contributions_for[v_player]:
                self.contributions_for[v_player][resource_changed] += amount
                self.contributions_for[v_player].update({"for": v_for})
            # if key not present set value to absolute of amount
            else:
                new_entry = {resource_changed: amount}
                self.contributions_for[v_player].update(new_entry)
                self.contributions_for[v_player].update({"for": v_for})
        # if key not in parent dictionary, make new key:value using abs amount
        else:
            new_entry = {resource_changed: amount}
            self.contributions_for.update({v_player: new_entry})
            self.contributions_for[v_player].update({"for": v_for})

        # check contributions haven't made player contribute negative quanitity
        # will have assigned the negative value already
        # not sure how to fix this
        if self.contributions_for[v_player][resource_changed] < 0:
            raise (ContributionError)

        return (output)

    @classmethod
    def make_all_debates(cls, file_path):
        """Reads all the information from debate cards csv and turns into cards

        Arguments:
            file_path = string

        Side Effects:
            Card instances stored in the class variable debate_cards.

        Dependencies:
            Uses reader from import csv.

        Returns:
            FileNotFoundError if can not file_path file
            PermissionError if filepath leads to disallowed area
            Else None
        """
        with open(file_path, "r", newline="") as card_file:
            file_reader = reader(card_file, delimiter=",")
            for line in file_reader:
                # This will exclude headers, empty lines and crisis cards
                if len(line) > 3:
                    # Need to take an uknown number of affected factions and
                    # turn them into a dictionary
                    aff_factions = {}
                    for data in line:
                        # format of data in csv is f for for and a for against
                        # followed by the name of the faction
                        # data[0] checks if the first letter is applicable
                        # data[1:] takes name of faction from whats left
                        if data[0] == "f":
                            new_entry = {str(data[1:]): True}
                        elif data[0] == "a":
                            new_entry = {str(data[1:]): False}
                        aff_factions.update(new_entry)
                    # make a new debate card with the data taken from the line
                    card = DebateCard(line[0], line[1], line[2], aff_factions)
                    DebateCard.debate_cards.append(card)


class Game:

    """Administrator Class."""

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
        # check given_rounds is int, otherwise assign
        try:
            if type(given_rounds) != int:
                raise (TypeError)
            if given_rounds > 0:
                self.total_rounds = given_rounds
            else:
                raise (ZeroError)
        except (TypeError):
            print("given_rounds must be of type int.")
        except (ZeroError):
            print(ZeroError.message)

        # iterate through dict to check player and faction befor assign
        self.set_of_players = set()
        self.factions_used = set()
        try:
            for key, value in dict_of_players.items():
                if self.player_available(value):
                    if self.faction_available(key):
                        new_player = Player(key, value)
                        self.set_of_players.add(new_player)
                        self.factions_used.add(value)
        except (FactionUsedError):
            print(FactionUsedError.message)
        except (PlayerNameError):
            print(PlayerNameError.message)
        except (AttributeError):
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
            raise (PlayerNameError)
        else:
            return (True)

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
            raise (NotFactionError)
        else:
            if country in self.factions_used:
                raise (FactionUsedError)
        return (True)

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
        # check for game end
        if self.current_round > self.total_rounds:
            output = False
        # otherwise reset the game cards
        else:
            for card in self.cards_in_play:
                self.cards_used.add(card)
            self.new_debate_cards()
        return (output)

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
                if output is False:
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
        return (check)

    def make_debate_con(self, player, card, v_for, resource, amount=1):
        """
        ############################################################################################
        #This was me trying to make a massive method to handle all votes.
        #I think it makes sense to start simpler.
        #TEMP
        """
        # Separate try blocks to avoid multiple errors of the same type
        output = ""
        try:
            if card not in self.cards_in_play:
                raise (NotValidCard)
            if type(v_for) != bool:
                raise (TypeError)
            if resource not in Rulebook.colours:
                raise (NotColourError)
        except (NotValidCard):
            output = NotValidCard.message
        except (TypeError):
            output = "argument voting-for must be of type boolean"
        except (NotColourError):
            output = "resources_used must be in Rulebook.colours"
        except (Exception):
            output = "Something unexpected occured checking input arguments"
        else:
            try:
                resource_legal = card.can_use_resource(resource)
                vote_legal = player.check_resource(resource, amount)
                if vote_legal and resource_legal:
                    player.increment_resource((-resource), amount)
                    card.change_contribution(v_for, player, resource, amount)
            except (ZeroError):
                output = "resources_used value must not be less than 1"
            except (TypeError):
                output = "resources_used value must be of type int."
            except (NotColourError):
                output = "resources key must be in Rulebook.colours."
            except (NotSuitableError):
                output = "Key of resources_used matched target card colour."
            except (ContributionError):
                output = ContributionError.message
            except (Exception):
                output = "Something unexpected happened"
        if len(output) == 0:
            return (f"{player} successfully contributed to {card.name}")
