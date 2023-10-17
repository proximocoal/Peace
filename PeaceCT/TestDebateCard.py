import unittest
from DebateCard import DebateCard
from NotColourError import NotColourError
from ZeroError import ZeroError
from NotFactionError import NotFactionError
from Player import Player

#####INCOMPLETE#######


class TestDebateCard(unittest.TestCase):

    def setUp(self):
        self.test_card = DebateCard("red", "test", "high", {"UK": True, "US": False})
        self.test_player = Player

    def tearDown(self):
        del self.test_card
    
    def test_real_faction_raise(self):
        #pass must be successful for setUp to run so only testing raising error
        with self.assertRaises(NotFactionError):
            self.test_card.real_faction("fish")
    
    def test_return_faction_impact_for(self):
        self.assertEqual (self.test_card.return_faction_impact("true"), [{"US"}, "red", 2])
    
    def test_return_faction_impact_against(self):
        self.assertEqual (self.test_card.return_faction_impact("false"), [{"UK"}, "red", 2])

    def test_return_faction_impact_raise(self):
        with self.assertRaises(TypeError):
            self.test_card.return_faction_impact("e")

    def test_change_contribution_int_error(self):
        with self.assertRaises(TypeError):
            self.test_card.change_contribution(True, "Connor", "blue", "w")

    def test_change_contribution_col_error(self):
        with self.assertRaises(NotColourError):
            self.test_card.change_contribution(True, "Connor", "Connor", 1)
    
    def test_change_contribution_int_error(self):
        with self.assertRaises(TypeError):
            self.test_card.change_contribution(True, "Connor", "blue", "w")

    def test_change_contribution_new_value(self):
        self.test_card.change_contribution(True, "Connor", "blue", 1)
        assert self.test_card.contributions_for == {"Connor": {"blue": 1}}
