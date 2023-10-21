import unittest
import unittest.mock
from CPlayerInterface import CPlayerInterface
from Rulebook import Rulebook
from Player2 import Player


class TestCPlayerInterface(unittest.TestCase):

    too_high = CPlayerInterface.num_of_factions + 1
    faction_list = []
    for faction in Rulebook.factions:
        faction_list.append(faction)
    faction = faction_list[0]

    def setUp(self):
        self.test = CPlayerInterface()

    def tearDown(self):
        del self.test

    def test_init_repeat_count(self):
        assert self.test.repeat_count == 0

    def test_init_human_players(self):
        assert self.test.human_players == 0

    def test_init_ai_players(self):
        assert self.test.ai_players == 0

    def test_init_player_list(self):
        assert self.test.player_list == []

    def test_init_available_factions(self):
        assert self.test.available_factions == Rulebook.factions

    def test_repeat_question_false(self):
        assert self.test.repeat_question(("a", "b", "c"), "a") is False
        assert self.test.repeat_count == 0

    def test_repeat_question_true(self):
        assert self.test.repeat_question(("a"), "b") is True
        assert self.test.repeat_count == 1

    def test_repeat_question_false_repeat(self):
        self.test.repeat_count = 11
        assert self.test.repeat_question(("a"), "a") is False
        assert self.test.repeat_count == 11

    def test_repeat_question_true_repeat(self):
        self.test.repeat_count = 11
        assert self.test.repeat_question(("a"), "b") is None
        assert self.test.repeat_count == 11

    @unittest.mock.patch("builtins.input", return_value="yes")
    def test_new_game_yes(self, mock_input):
        assert self.test.new_game() is True
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="NO")
    def test_new_game_no(self, mock_input):
        assert self.test.new_game() is False
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="y")
    def test_new_game_repeat_wrong(self, mock_input):
        assert self.test.new_game() is True
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="")
    def test_new_game_empty(self, mock_input):
        assert self.test.new_game() is True
        assert self.test.repeat_count == 0

    def test_convert_to_bool_yes(self):
        assert self.test.convert_to_bool("yes") is True

    def test_convert_to_bool_no(self):
        assert self.test.convert_to_bool("NO") is False

    def test_convert_to_bool_empty(self):
        assert self.test.convert_to_bool("") == ""

    def test_convert_to_bool_wrong(self):
        assert self.test.convert_to_bool("FISH") == "fish"

    @unittest.mock.patch("builtins.input", return_value="1")
    def test_how_many_humans_good(self, mock_input):
        self.test.how_many_humans()
        assert self.test.human_players == 1
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="0")
    def test_how_many_humans_zero(self, mock_input):
        self.test.how_many_humans()
        assert self.test.human_players == CPlayerInterface.default_human
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value=too_high)
    def test_how_many_humans_high(self, mock_input):
        self.test.how_many_humans()
        assert self.test.human_players == CPlayerInterface.default_human
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="fish")
    def test_how_many_humans_string(self, mock_input):
        self.test.how_many_humans()
        assert self.test.human_players == CPlayerInterface.default_human
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="")
    def test_how_many_humans_empty(self, mock_input):
        self.test.how_many_humans()
        assert self.test.human_players == CPlayerInterface.default_human
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="0")
    def test_how_many_ai_good(self, mock_input):
        self.test.how_many_ai()
        assert self.test.ai_players == 0
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value=too_high)
    def test_how_many_ai_high(self, mock_input):
        self.test.how_many_ai()
        assert self.test.ai_players == CPlayerInterface.default_ai
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="-1")
    def test_how_many_ai_minus(self, mock_input):
        self.test.how_many_ai()
        assert self.test.ai_players == CPlayerInterface.default_ai
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="fish")
    def test_how_many_ai_string(self, mock_input):
        self.test.how_many_ai()
        assert self.test.ai_players == CPlayerInterface.default_ai
        assert self.test.repeat_count == 0

    def test_make_range(self):
        out = self.test.make_range()
        assert CPlayerInterface.num_of_factions in out
        assert (CPlayerInterface.num_of_factions + 1) not in out

    @unittest.mock.patch("builtins.input", return_value=faction)
    def test_which_faction_false_good(self, mock_input):
        CPlayerInterface.auto_faction = False
        faction = TestCPlayerInterface.faction
        assert self.test.which_faction() == faction
        assert faction not in self.test.available_factions
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value=faction)
    def test_which_faction_false_used(self, mock_input):
        CPlayerInterface.auto_faction = False
        faction = TestCPlayerInterface.faction
        self.test.available_factions.discard(faction)
        assert self.test.which_faction() == ""
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="fish")
    def test_which_faction_false_bad(self, mock_input):
        CPlayerInterface.auto_faction = False
        assert self.test.which_faction() == ""
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="fish")
    def test_which_faction_true_bad(self, mock_input):
        CPlayerInterface.auto_faction = True
        out = self.test.which_faction()
        difference = Rulebook.factions.difference(self.test.available_factions)
        assert out == difference.pop()
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value=faction)
    def test_which_faction_true_good(self, mock_input):
        CPlayerInterface.auto_faction = True
        faction = TestCPlayerInterface.faction
        assert self.test.which_faction() == faction
        assert faction not in self.test.available_factions
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="")
    def test_which_faction_true_empty(self, mock_input):
        CPlayerInterface.auto_faction = True
        out = self.test.which_faction()
        difference = Rulebook.factions.difference(self.test.available_factions)
        assert out == difference.pop()
        assert self.test.repeat_count == 0

    def test_ran_faction(self):
        out = self.test.ran_faction()
        self.test.available_factions.discard(out)
        difference = Rulebook.factions.difference(self.test.available_factions)
        assert out == difference.pop()

    def test_min_num_players_human_only(self):
        self.test.human_players = CPlayerInterface.minimum_players
        assert self.test.min_num_players() is True

    def test_min_num_players_mix(self):
        self.test.human_players = CPlayerInterface.minimum_players
        ai = CPlayerInterface.num_of_factions - self.test.human_players
        self.test.ai_players = ai
        assert self.test.min_num_players() is True

    def test_min_num_players_too_low(self):
        assert self.test.min_num_players() is False

    def test_min_num_players_too_high(self):
        self.test.human_players = TestCPlayerInterface.too_high
        assert self.test.min_num_players() is False

    @unittest.mock.patch("builtins.input", return_value=faction)
    @unittest.mock.patch.object(Player, '__new__')
    def test_make_player_human(self, mock_player, mock_input):
        self.test.make_player(1, True)
        faction = TestCPlayerInterface.faction
        mock_player.assert_called_with(Player, faction, faction, True)

    @unittest.mock.patch("builtins.input", return_value=faction)
    @unittest.mock.patch.object(Player, '__new__')
    def test_make_player_ai(self, mock_player, mock_input):
        self.test.make_player(1, False)
        faction = TestCPlayerInterface.faction
        mock_player.assert_called_with(Player, faction, faction, False)

    @unittest.mock.patch("builtins.input", return_value="yes")
    def test_define_player_yes(self, mock_input):
        assert self.test.define_player(1) is True
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="no")
    def test_define_player_no(self, mock_input):
        assert self.test.define_player(1) is False
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="")
    def test_define_player_empty(self, mock_input):
        assert self.test.define_player(1) is True
        assert self.test.repeat_count == 0

    @unittest.mock.patch("builtins.input", return_value="fish")
    def test_define_player_wrong(self, mock_input):
        assert self.test.define_player(1) is True
        assert self.test.repeat_count == 0

    @unittest.mock.patch.object(CPlayerInterface, "make_player")
    def test_fill_player_list_human(self, mock_init):
        self.test.human_players = 1
        self.test.fill_player_list()
        mock_init.assert_called_with(1, True)

    @unittest.mock.patch("builtins.input", return_value="no")
    @unittest.mock.patch.object(CPlayerInterface, "make_player")
    def test_fill_player_list_ai(self, mock_init, mock_input):
        self.test.ai_players = 1
        self.test.fill_player_list()
        mock_init.assert_called_with(1, False)

    @unittest.mock.patch("builtins.input", return_value="no")
    @unittest.mock.patch.object(CPlayerInterface, "make_player")
    def test_fill_player_list_multiple(self, mock_init, mock_input):
        self.test.ai_players = 1
        self.test.human_players = 1
        self.test.fill_player_list()
        assert mock_init.call_count == 2

    @unittest.mock.patch.object(CPlayerInterface, "how_many_humans")
    @unittest.mock.patch.object(CPlayerInterface, "how_many_ai")
    @unittest.mock.patch.object(CPlayerInterface, "min_num_players", return_value=True)
    @unittest.mock.patch.object(CPlayerInterface, "fill_player_list")
    def test_player_coordinator(self, mock_list, mock_num, mock_ai, mock_hum):
        self.test.player_coordinator()
        mock_list.assert_called()
        mock_num.assert_called()
        mock_ai.assert_called()
        mock_hum.assert_called()
