import unittest
from Player import Player

class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.new_player = Player("UK", "Connor")

    def tearDown(self):
        del self.new_player

    def test_repr_pass(self):
        assert str(self.new_player) == "Class: Player, name: Connor"
    
    def test_increment_resource_pass(self):
        self.new_player.increment_resource("red", 1)
        assert self.new_player.resources["red"] == 1
        assert self.new_player.resources["blue"] == 0
        assert self.new_player.resources["yellow"] == 0
    
    @unittest.expectedFailure
    def test_increment_resource_fail_int(self):
        self.new_player.increment_resource("red", "fish")
        assert self.new_player.resources["red"] == "fish"
        assert self.new_player.resources["blue"] == 0
        assert self.new_player.resources["yellow"] == 0
    
    @unittest.expectedFailure
    def test_increment_resource_fail_col(self):
        self.new_player.increment_resource("Red", 1)
        assert self.new_player.resources["red"] == 1
        assert self.new_player.resources["blue"] == 0
        assert self.new_player.resources["yellow"] == 0
    
    def test_check_loss_none(self):
        assert self.new_player.check_loss() == True
    
    def test_check_loss_false(self):
        self.new_player.increment_resource("yellow", 1)
        self.new_player.increment_resource("blue", 1)
        self.new_player.increment_resource("red", 1)
        assert self.new_player.check_loss() == False
    
    def test_check_resource_true(self):
        self.new_player.increment_resource("red", 1)
        assert self.new_player.check_resource("red", 1) == True
    
    def test_check_resource_false(self):
        assert self.new_player.check_resource("yellow", 1) == False
    
    @unittest.expectedFailure
    def test_check_resource_zero(self):
        assert self.new_player.check_resource("blue", 0) == True
    
    @unittest.expectedFailure
    def test_check_resource_int(self):
        assert self.new_player.check_resource("red", "blue") == False

if __name__ == "__main__":
    unittest.main()