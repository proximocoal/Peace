import unittest
from Rulebook import Rulebook
from NotFactionError import NotFactionError
from NotColourError import NotColourError
from NotSeverityError import NotSeverityError

class TestRulebook(unittest.TestCase):

    def test_is_faction_true(self):
        assert Rulebook.is_faction("UK") == True
    
    def test_is_faction_fail(self):
        with self.assertRaises(NotFactionError):
            Rulebook.is_faction(True)
    
    def test_is_colour_true(self):
        assert Rulebook.is_colour("blue") == True
    
    def test_is_colour_fail(self):
        with self.assertRaises(NotColourError):
            Rulebook.is_colour(True)
    
    def test_is_severity_true(self):
        assert Rulebook.is_severity("high") == True
    
    def test_is_severity_fail(self):
        with self.assertRaises(NotSeverityError):
            Rulebook.is_severity(True)
    
    def test__repr__(self):
        self.assertEqual(Rulebook.__repr__(), (f"""
        factions: {Rulebook.factions}
        colours: {Rulebook.colours}
        base_resources: {Rulebook.base_resources}
        severity: {Rulebook.severity}
        severity_impact: {Rulebook.severity_impact}
        """))

if __name__ == "__main__":
    unittest.main()