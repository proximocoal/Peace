from Rulebook import Rulebook
from Player2 import Player
import random


class CPlayerInterface():
    """
    Use input function to make list of player objects for Peace game.

    Class Variables:
        num_of_factions = set of strings - iterable of factions in game
        max_repeat = int - how often to ask a question before skipping
        minimum_players = int - how many players needed for game to work
        default_human = int - how many human players if no answer given
        default_ai = int - how many ai if no answer given
        auto_faction = bool - if True will assign faction if input not given

    Instance Variables:
        repeat_count = int - used to track how many times a question is asked
        human_players = int - how many human players are input
        ai_players = int - how many ai players are input
        available_factions = set of strings - tracks available factions
        player_list = list of player objects

    Instance methods:
        __init__() - initialiser
        new_game() - ask if user wants a new game
        convert_to_bool() - turns string into bool
        repeat_question() - return true or false based on attempts
        how_many_humans() - ask how many human players wanted
        how_many_ai() - ask how many ai players wanted
        which_factions() - assigns a faction to a player
        min_num_players() - checks number of players suitable
        make_player() - returns a player object based on input
        define_player() - set player to human or ai based on input
        fill_player_list() - populate player list with player objects
        player_coordinator() - Calls instance methods to complete player setup
        make_range() - Return set of numbers 0 - num_of_factions and ""
        ran_faction() -Return a random faction from available_factions

    Dependencies:
        Rulebook
        Player2
    """

    num_of_factions = len(Rulebook.factions)
    max_repeat = 10
    minimum_players = 3
    default_human = minimum_players
    default_ai = 0
    auto_faction = True

    def __init__(self):
        self.repeat_count = 0
        self.human_players = 0
        self.ai_players = 0
        self.available_factions = set()
        for faction in Rulebook.factions:
            self.available_factions.add(faction)
        self.player_list = []

    def new_game(self):
        """
        Ask if user would like to start a new game.

        Arguments:
            Self

        Returns:
            If input is yes return True.
            If input is no return False.
            Otherwise repeat question.
            Default True if left empty or too many attempts

        Dependencies:
            self.convert_to_bool()
            self.repeat_question()
            self.repeat_count
            CLInterface.max_repeat
        """
        repeat = True
        while repeat is True:
            answer = input("""Would you like to start a new game?
                       Enter yes, no or leave empty to escape.""")
            answer = self.convert_to_bool(answer)
            repeat = self.repeat_question((True, False, ""), answer)
        if repeat is None or answer == "":
            answer = True
        self.repeat_count = 0
        return (answer)

    def convert_to_bool(self, bool_string):
        """
        Convert input to boolean value.

        Arguments:
            bool_string - must be string else error raised

        Returns:
            If bool_string is yes return True,
            If no return False, else return string in lower case

        Dependencies:
            builtins - string.lower()
        """
        bool_string = bool_string.lower()
        if bool_string == "yes":
            bool_string = True
        elif bool_string == "no":
            bool_string = False
        return (bool_string)

    def repeat_question(self, acceptable_values, given_value):
        """
        Check given_value is in acceptable_values.

        Arguments:
            acceptable_values - must be iterable or error raised
            given_value

        Returns:
            If given_value is in acceptable_values return False.
            Else if self.repeat_count is greater than max_repeat, return None.
            Else increase self.repeat_count by 1 and return True

        Dependencies:
            self.repeat_count
            builtins - in

        Side Effects:
            self.repeat_count set to 0
        """
        output = True
        if given_value in acceptable_values:
            output = False
        elif self.repeat_count > CPlayerInterface.max_repeat:
            output = None
        else:
            self.repeat_count += 1
        return (output)

    def make_range(self):
        """
        Make a set with values "" and integers 0 to num_of_factions

        Returns:
            set

        Dependencies:
            CPlayerInterface.num_of_factions
        """
        count = 0
        collection = set("")
        while count <= CPlayerInterface.num_of_factions:
            collection.add(count)
            count += 1
        return (collection)

    def how_many_humans(self):
        """
        Get input for total number of human players.

        Side Effects:
            self.human_players set to integer between 1 and num_of_factions
            Default to default_human if input empty or too many attempts
            self.repeat_count set to 0

        Dependencies:
            CPlayerInterface.num_of_factions
            self.repeat_question()
            self.repeat_count
            ValueError
            self.human_players
            self.make_range()
            CPlayerInterface.default_human
        """
        repeat = True
        collection = self.make_range()
        # must be at least one human player
        collection.discard(0)
        while repeat is True:
            output = input(f"""How many human players do you want?
                           Please enter a whole number
                           between 1 and {CPlayerInterface.num_of_factions}.
                           Leave the input empty to escape.""")
            try:
                output = int(output)
            except (ValueError):
                pass
            repeat = self.repeat_question(collection, output)
        if repeat is None or output == "":
            output = CPlayerInterface.default_human
        self.repeat_count = 0
        self.human_players = output

    def how_many_ai(self):
        """
        Get input for total number of ai players.

        Side Effects:
            self.ai_players set to integer between 0 and max_ai
            where max_ai is equal to num_of_factions - human_players
            Default to default_ai if input empty or too many attempts.
            self.repeat_count set to 0

        Dependencies:
            CPlayerInterface.num_of_factions
            CPlayerInterface.default_ai
            self.human_players
            self.ai_players
            self.repeat_count
            self.repeat_question()
            ValueError
            self.make_range()
        """
        repeat = True
        collection = self.make_range()
        max_ai = CPlayerInterface.num_of_factions - self.human_players
        while repeat is True:
            output = input(f"""How many AI players do you want?
                            Please enter a whole number between 0 and {max_ai}
                            Leave the input empty to escape.""")
            try:
                output = int(output)
            except (ValueError):
                pass
            repeat = self.repeat_question(collection, output)
        if repeat is None or output == "":
            output = CPlayerInterface.default_ai
        self.repeat_count = 0
        self.ai_players = output

    def ran_faction(self):
        """
        Return a random faction from available_factions

        Returns:
            string

        Dependencies:
            random.choice()
            self.available_factions()
        """
        faction_list = []
        for faction in self.available_factions:
            faction_list.append(faction)
        out = random.choice(faction_list)
        return (out)

    def which_faction(self):
        """
        Get input for which faction.

        Returns:
            string from self.available_factions or empty string

        Side Effects:
            remove chosen value from self.available_factions
            self.repeat_count set to 0

        Dependencies:
            self.available_factions
            self.repeat_count
            self.repeat_question()
            self.ran_faction()
            CPlayerInterface.auto_faction
        """
        repeat = True
        collection = set()
        for faction in self.available_factions:
            collection.add(faction)
        collection.add("")
        while repeat is True:
            out = input(f"""Which faction would you like for this player?
                           Please enter one of the following:
                           {self.available_factions}
                           leave the input empty to escape.""")
            repeat = self.repeat_question(collection, out)
        if repeat is None:
            out = ""
        if out == "" and CPlayerInterface.auto_faction:
            out = self.ran_faction()
        self.available_factions.discard(out)
        self.repeat_count = 0
        return (out)

    def min_num_players(self):
        """Check ai_players + human_players is within acceptable range.

        Return:
            Bool

        Dependencies:
            self.ai_players
            self.human_players
            CLInterface.minimum_players
            CLInterface.num_of_factions
        """
        output = False
        total_players = self.ai_players + self.human_players
        max = CPlayerInterface.num_of_factions + 1
        if total_players in range(CPlayerInterface.minimum_players, max):
            output = True
        return (output)

    def make_player(self, count, is_human):
        """
        Initialise Player object.

        Arguments:
            count - int
            human - bool

        Returns:
            Player Object

        Dependencies:
            self.make_players()
            self.which_faction()
            Player.__init__()
        """
        race = "human"
        if is_human is False:
            race = "computer"
        print(f"Player:{count}, {race}")
        faction_choice = self.which_faction()
        name_given = input(f"Please enter a name for Player:{count}")
        new_player = Player(faction_choice, name_given, is_human)
        return (new_player)

    def define_player(self, count):
        """
        Take user input to define if player is human or not.

        Arguments:
            count = int

        Returns:
            bool
            default value is true

        Side Effects:
            self.repeat_count set to 0

        Dependencies:
            self.repeat_question()
            self.repeat_count
        """
        repeat = True
        output = True
        player_race = ""
        while repeat:
            player_race = input(f"""Would you like player {count} to be AI?
                            enter yes, no or leave empty to escape.""")
            repeat = self.repeat_question(("yes", "no", ""), player_race)
        player_race = self.convert_to_bool(player_race)
        if player_race is False:
            output = False
        self.repeat_count = 0
        return (output)

    def fill_player_list(self):
        """
        Populate player_list with Player objects.

        Side Effects:
            self.player_list filled with Player objects

        Dependencies:
            self.player_list
            self.human_players
            self.ai_players
            self.define_player()
            self.make_player()
        """
        player_range = range(1, (self.human_players+self.ai_players+1))
        reg_ai = 0
        count = 1
        for i in player_range:
            is_human = True
            if reg_ai < self.ai_players:
                is_human = self.define_player(count)
            if is_human is False:
                reg_ai += 1
            new_player = self.make_player(count, is_human)
            self.player_list.append(new_player)
            count += 1

    # Does not incorportate default values
    def player_coordinator(self):
        """
        Define how many of each player type and fill player list.

        Dependencies:
            self.how_many_humans()
            self.how_many_ai()
            self.min_num_players()
            self.fill_player_list()
        """
        players_set = False
        while players_set is False:
            self.how_many_humans()
            self.how_many_ai()
            if self.human_players == "" or self.ai_players == "":
                players_set = None
            else:
                players_set = self.min_num_players()
        if players_set:
            self.fill_player_list()
