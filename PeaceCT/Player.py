from xmlrpc.client import boolean
from Rulebook import Rulebook
from ZeroError import ZeroError
from NotColourError import NotColourError


class Player:
    """Represents the human players who take part in the game.

    Instance Variables:
        self.resources - dictionary - the currency players can use in game
        self.user_faction - string - the country the player controls
        self.player_name - string - name of the player
        c1_votes - dict - player votes and contribution of each resource
        c2_votes - dict - player votes and contribution of each resource
        c3_votes - dict - player votes and contribution of each resource

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
            Rulebook
        """

        if Rulebook.is_faction(faction_choice) is True:
            self.user_faction = faction_choice
        self.player_name = name_given
        self.resources = {"red": 0, "yellow": 0, "blue": 0}
        self.c1 = {"for": None, "red": 0, "yellow": 0, "blue": 0}
        self.c2 = {"for": None, "red": 0, "yellow": 0, "blue": 0}
        self.c3 = {"for": None, "red": 0, "yellow": 0, "blue": 0}

    def __repr__(self):
        """Return player_name and name of class when called as string"""
        return (f"Class: Player, name: {self.player_name}")

    def increment_resource(self, colour, amount):
        """Change the values of self.resources by quantity of amount.

        Arguments:
            colour - string - should be key in resources
            amount - int - with accompanying signage (e.g. -)

        Side Effects:
            resources - key input_colour changed by amount

        Return:
            new value of changed resource
        """
        self.resources[colour] += amount
        return (self.resources[colour])

    def check_loss(self):
        """check if any values in resources are less than 1. Return boolean."""
        output = False
        for value in self.resources.values():
            if value < 1:
                output = True
        return (output)

    def check_resource(self, colour, amount):
        """Check player has resource with value not less than quanitity.

        Arguments:
            colour = string - should be in Rulebook.colours
            amount = int - must be non-zero integer

        Returns:
            If resource value >= quantity returns True, else False
        """
        output = True
        if self.resources[colour] + amount < 0:
            output = False
        return (output)

    def validate_resource(self, colour, amount):
        """Perform validation for self.change_resource.

        Arguments:
            colour = string - must be in Rulebook.colours
            amount = int - must be non-zero integer

        Returns:
            NotColourError if colour incorrect
            ZeroError if amount incorrect
            Else True

        Dependencies:
            ZeroError, Rulebook.colours, NotColourError
        """
        if type(amount) != int or amount == 0:
            raise (ZeroError)
        if colour not in Rulebook.colours:
            raise (NotColourError)
        return (True)

    def change_resource(self, colour, amount):
        """Modify the value of self.resource[colour] by amount with checks.

        Arguments:
            colour = string - must be in Rulebook.colours
            amount = int - must be non-zero integer

        Returns:
            NotColourError if colour incorrect
            ZeroError if amount incorrect
            False if operation unsuccessful
            Else new value of self.resource[colour]

        Dependencies:
            self.validate_resource
            self.check_resource
            self.increment_resource
            Rulebook.colours
            ZeroError
            NotColourError

        Side Effects:
            change value of self.resource[colour]
        """
        self.validate_resource(colour, amount)
        output = self.check_resource(colour, amount)
        if output is True:
            output = self.increment_resource(colour, amount)
        return (output)

    def swap_vote(self, card, bool):
        """Check if player has voted opposite on the card previously.

        Arguments:
            card = string - must be "c1", "c2" or "c3"
            bool = boolean - must be True or False

        Returns:
            If bool is not equal self.c1/c2/c3["for"] then True, else False
        """
        output = False
        if card == "c1":
            if self.c1["for"] != bool:
                output = True
        elif card == "c2":
            if self.c2["for"] != bool:
                output = True
        elif card == "c3":
            if self.c3["for"] != bool:
                output = True
        return (output)

    def refund_contributions(self, card):
        """Add the value of contributions back to player and set to 0.

        Arguments:
            Arguments:
            card = string - must be "c1", "c2" or "c3"

        Dependencies:
            Uses self.check_is_card,
            self.increment_resource,
            Rulebook.colours.

        Side Effects:
            Increase the value of self.resources for each different colour
        """
        if card == "c1":
            for key in self.c1:
                if key in Rulebook.colours:
                    self.increment_resource(key, self.c1[key])
                    self.c1[key] = 0
        elif card == "c2":
            for key in self.c1:
                if key in Rulebook.colours:
                    self.increment_resource(key, self.c1[key])
                    self.c1[key] = 0
        elif card == "c3":
            for key in self.c1:
                if key in Rulebook.colours:
                    self.increment_resource(key, self.c1[key])
                    self.c1[key] = 0

    def check_contribution(self, card, colour, amount):
        """Check the card has the contribution in the given amount

        Arguments:
            card = string - must be "c1", "c2" or "c3"
            colour = string - must be in Rulebook.colours
            amount = int - must be int

        Returns:
            True if self.c1/c2/c3[colour] + amount >= 0, else False

        Dependencies:
            Rulebook.colours, ZeroError, NotColourError
        """
        output = False
        if card == "c1":
            if self.c1[colour] + amount >= 0:
                output = True
        elif card == "c2":
            if self.c2[colour] + amount >= 0:
                output = True
        elif card == "c3":
            if self.c3[colour] + amount >= 0:
                output = True
        return (output)

    def increment_card_resource(self, card, colour, amount):
        """Change self.card[colour] by amount

        Arguments:
            card = string - must be "c1", "c2" or "c3"
            colour = string - must be in Rulebook.colours
            amount = int - must be int

        Returns:
            if colour not key in self.resources
            True if operation succeeds, else False

        Side Effects:
            Change self.card[colour] by amount

        Dependencies:
            Rulebook.colours, self.check_contribution
        """
        output = True
        if card == "c1":
            self.c1[colour] += amount
        elif card == "c2":
            self.c2[colour] += amount
        elif card == "c3":
            self.c3[colour] += amount
        else:
            output = False
        return (output)

    def validate_contribution(self, card, vote_for, colour, amount):
        """Check input values are suitable.

        Arguments:
            card = string - must be "c1", "c2" or "c3" else KeyError
            vote_for = bool else TypeError
            colour = string - must be in Rulebook.colours else NotColourError
            amount = int - must be non-zero int else ZeroError

        Returns:
            KeyError if card incorrect
            NotColourError if colour incorrect
            TypeError if vote_for incorrect
            ZeroError if amount incorrect
            Else True

        Dependencies:
            Rulebook.colours, NotColourError, ZeroError
        """
        if card not in {"c1", "c2", "c3"}:
            raise (KeyError)
        if type(vote_for) != boolean:
            raise (TypeError)
        if colour not in Rulebook.colours:
            raise (NotColourError)
        if type(amount) != int or amount == 0:
            raise (ZeroError)
        return (True)

    def set_vote(self, card, vote_for):
        """Change the value of self.card["for"] to vote_for"""
        if card == "c1":
            self.c1["for"] = vote_for
        elif card == "c2":
            self.c2["for"] = vote_for
        elif card == "c3":
            self.c3["for"] = vote_for

    def change_contributions(self, card, vote_for, colour, amount):
        """Deduct amount from self.resource[colour] add to self.card[colour] with checks

        Arguments:
            card = string - must be "c1", "c2" or "c3"
            vote_for = bool else TypeError
            colour = string - must be in Rulebook.colours
            amount = int - must be non-zero int

        Returns:
            KeyError if card incorrect
            NotColourError if colour incorrect
            TypeError if vote_for incorrect
            ZeroError if amount incorrect
            If contribution will result in less than 0 resource, return False
            If contribution will result in less than 0 cont, return False
            If operation successful return True

        SideEffects:
            If self.c1/c2/c3[for] != vote_for:
                add contributions to self.resource
                change self.c1/c2/c3[for] to vote_for
            Deduct amount from self.resource[colour]
            add amount to self.c1/c2/c3[colour]

        Dependencies:
            self.increment_card_resource
            self.check_contribution
            self.check_resource
            self.refund_contribution
            self.validate_contribution
            self.swap_vote
            self.increment_resource
            self.set_vote
            Rulebook.colours
            ZeroError
            NotColourError
        """
        # check input values are suitable
        self.validate_contribution(card, vote_for, colour, amount)
        # check contribution change will not result in less than 0 value
        output = self.check_contribution(card, colour, amount)
        # check resource change will not result in less than 0 value
        output = self.check_resource(colour, -amount)
        # check if player voted opposite previously
        if output is True and self.swap_vote(card, vote_for) is True:
            # make sure contribution change positive for new vote
            if amount > 0:
                # reset player contribution, refund and change player vote
                self.refund_contributions(card)
                self.set_vote(card, vote_for)
            else:
                # do not continue with operation
                output = False
        if output is True:
            # remove value of contribution from player
            self.increment_resource(colour, -amount)
            # add value of contribution to card
            self.increment_card_resource(card, colour, amount)
        return (output)
