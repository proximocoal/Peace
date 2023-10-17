import unittest
from PeaceCard import PeaceCard
from NotColourError import NotColourError
from ZeroError import ZeroError


class TestPeaceCard(unittest.TestCase):

    def setUp(self):
        self.test_card = PeaceCard("test", "high", "red")
        self.test_card.contributions_for.update({"fred": {"yellow":0, "blue":0}, "george": {"yellow":0, "blue":0}})

    def tearDown(self):
        del self.test_card
    
    def test_can_use_resource_true(self):
        assert self.test_card.can_use_resource("blue") == True
    
    def test_can_use_resource_false(self):
        assert self.test_card.can_use_resource("red") == False
    
    def test_can_use_resource_error(self):
        with self.assertRaises(NotColourError):
            self.test_card.can_use_resource(1) 

    def test_get_impact(self):
        assert self.test_card.get_impact() == ("red", 2)
    
    def test_make_nested_dict(self):
        assert self.test_card.make_nested_dict() == {"yellow":0, "blue":0}
    
    def test_set_base_contributions(self):
        self.test_card.contributions_for = {}
        self.test_card.set_base_contributions(["fred", "george"])
        assert self.test_card.contributions_for == {"fred": {"yellow":0, "blue":0}, "george": {"yellow":0, "blue":0}}
    
    def test_check_all_contributions_false(self):
        self.test_card.contributions_for["fred"] = {"yellow":-1, "blue":0}
        assert self.test_card.check_all_contributions("fred") == False
    
    def test_check_all_contributions_true(self):
        assert self.test_card.check_all_contributions("fred") == True

    def test_check_contribution_change_false(self):
        assert self.test_card.check_contribution_change("fred", "yellow", -1) == False
    
    def test_check_contribution_change_error(self):
        assert self.test_card.check_contribution_change("fred", "red", 0) == False

    def test_check_contribution_change_pos(self):
        self.test_card.contributions_for.update({"fred": {"yellow":1, "blue":0}})
        assert self.test_card.check_contribution_change("fred", "yellow", -1) == True

    def test_change_contribution_true(self):
        assert self.test_card.change_contribution("fred", "yellow", 1) == True
    
    def test_change_contribution_negative(self):
        assert self.test_card.change_contribution("fred", "yellow", -1) == False
    
    def test_change_contribution_name(self):
        with self.assertRaises(KeyError):
            self.test_card.change_contribution("fish", "yellow", 1)
    
    def test_change_contribution_colour(self):
        with self.assertRaises(NotColourError):
            self.test_card.change_contribution("fred", "red", 1)
    
    def test_change_contribution_int(self):
        with self.assertRaises(TypeError):
            self.test_card.change_contribution("fred", "yellow", 1.1)
    
    def test_change_contribution_zero(self):
        with self.assertRaises(ZeroError):
            self.test_card.change_contribution("fred", "yellow", 0)
    
    def test__repr__(self):
        assert str(self.test_card) == "Class: Peace Card. Name: test"
    
    def test_show_contributions_pass(self):
        assert self.test_card.show_contributions("fred") == {"yellow":0, "blue":0}
    
    def test_show_contributions_raises(self):
        with self.assertRaises(KeyError):
            self.test_card.show_contributions("fish")
    
    def test_remove_contributions_pass(self):
        assert self.test_card.remove_contributions("fred") == {"yellow":0, "blue":0}
        assert self.test_card.contributions_for["fred"] == {}

    def test_remove_contributions_raise(self):
        with self.assertRaises(KeyError):
            self.test_card.remove_contributions("fish")
    
    @unittest.skip("stub for temp file creation method")
    def test_make_all_crisis(self):
        pass
    
