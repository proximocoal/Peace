import unittest
from Player import Player
from ZeroError import ZeroError
from NotColourError import NotColourError


class TestPlayer(unittest.TestCase):

    init_red = 2
    init_yellow = 1
    init_blue = 0
    init_c2_for = True
    init_c3_for = False
    init_c2c3_colour = 0

    def setUp(self):
        self.new_player = Player("UK", "Connor")
        self.new_player.resources["red"] = self.init_red
        self.new_player.resources["yellow"] = self.init_yellow
        self.new_player.c2["for"] = self.init_c2_for
        self.new_player.c3["for"] = self.init_c3_for
        self.new_player.c1["red"] = self.init_red
        self.new_player.c1["yellow"] = self.init_yellow

    def tearDown(self):
        del self.new_player

    def no_change(self):
        check = True
        if self.new_player.resources["red"] != self.init_red:
            check = False
        elif self.new_player.resources["yellow"] != self.init_yellow:
            check = False
        elif self.new_player.resources["blue"] != self.init_blue:
            check = False
        elif self.new_player.c1["red"] != self.init_red:
            check = False
        elif self.new_player.c1["yellow"] != self.init_yellow:
            check = False
        elif self.new_player.c1["blue"] == self.init_blue:
            check = False
        if check is True:
            for key, value in self.new_player.c2.items():
                if key != "for":
                    if value != self.init_c2c3_colour:
                        check = False
                        break
                else:
                    if value != self.init_c2_for:
                        check = False
        if check is True:
            for key, value in self.new_player.c3.items():
                if key != "for":
                    if value != self.init_c2c3_colour:
                        check = False
                        break
                else:
                    if value != self.init_c3_for:
                        check = False
        return (check)

    def test_repr_pass(self):
        assert str(self.new_player) == "Class: Player, name: Connor"

    def test_increment_resource_pass(self):
        assert self.new_player.increment_resource("red", 1) == self.init_red + 1
        assert self.new_player.resources["red"] == self.init_red + 1

    def test_increment_resource_fail_int(self):
        with self.assertRaises(RuntimeError):
            self.new_player.increment_resource("red", "fish")
        assert self.no_change() is True

    def test_increment_resource_fail_col(self):
        with self.assertRaises(KeyError):
            self.new_player.increment_resource("Red", 1)
        assert self.no_change() is True

    def test_check_loss_true(self):
        assert self.new_player.check_loss() is True

    def test_check_loss_false(self):
        # blue value is 0 in set up, which would result in True
        self.new_player.resources["blue"] = 1
        assert self.new_player.check_loss() is False

    def test_check_resource_true(self):
        assert self.new_player.check_resource("red", self.init_red) is True

    def test_check_resource_false(self):
        assert self.new_player.check_resource("yellow", self.init_yellow + 1) is False

    def test_check_resource_error_amount(self):
        with self.assertRaises(RuntimeError):
            self.new_player.check_resource("red", "yellow")

    def test_check_resource_error_colour(self):
        with self.assertRaises(KeyError):
            self.new_player.increment_resource("Red", 1)

    def test_validate_resource_pass(self):
        assert self.new_player.validate_resource("red", self.init_red)

    def test_validate_resource_zero(self):
        with self.assertRaises(ZeroError):
            self.new_player.validate_resource("red", 0)

    def test_validate_resource_int(self):
        with self.assertRaises(ZeroError):
            self.new_player.validate_resource("red", "yellow")

    def test_validate_resource_colour(self):
        with self.assertRaises(NotColourError):
            self.new_player.validate_resource("Red", 1)

    def test_change_resource_pass_pos(self):
        assert self.new_player.change_resource("red", 1) == self.init_red + 1
        assert self.new_player.resources["red"] == self.init_red + 1

    def test_change_resource_pass_neg(self):
        assert self.new_player.change_resource("red", -1) == self.init_red - 1
        assert self.new_player.resources["red"] == self.init_red - 1

    def test_change_resource_error_zero(self):
        with self.assertRaises(ZeroError):
            self.new_player.change_resource("red", 0)
        assert self.no_change() is True

    def test_change_resource_error_int(self):
        with self.assertRaises(ZeroError):
            self.new_player.change_resource("red", "yellow")
        assert self.no_change() is True

    def test_change_resource_error_colour(self):
        with self.assertRaises(NotColourError):
            self.new_player.change_resource("Red", 0)
        assert self.no_change() is True

    def test_change_resource_fail(self):
        assert self.new_player.change_resource("blue", -1) is False
        assert self.no_change() is True

    def test_swap_vote_none(self):
        assert self.new_player.swap_vote("c1", False) is True

    def test_swap_vote_true(self):
        assert self.new_player.swap_vote("c2", not self.init_c2_for) is True

    def test_swap_vote_false(self):
        assert self.new_player.swap_vote("c2", self.init_c2_for) is False

    def test_refund_contributions_some(self):
        self.new_player.refund_contributions("c1")
        assert self.new_player.resources["red"] == self.init_red + self.init_red
        assert self.new_player.resources["yellow"] == self.init_yellow + self.init_yellow
        assert self.new_player.resources["blue"] == self.init_blue + self.init_blue

    def test_refund_contributions_empty(self):
        self.new_player.refund_contributions("c2")
        assert self.no_change() is True

    def test_refund_contributions_not_card(self):
        self.new_player.refund_contributions("c4")
        assert self.no_change() is True

    def test_check_contribution_true(self):
        assert self.new_player.check_contribution("c1", "red", self.init_red) is True

    def test_check_contribution_false(self):
        assert self.new_player.check_contribution("c1", "red", self.init_red + 1) is False

    def test_check_contribution_neg(self):
        assert self.new_player.check_contribution("c3", "red", -self.init_red) is True

    def test_increment_card_resource_true(self):
        assert self.new_player.increment_card_resource("c1", "red", 1) is True
        assert self.new_player.c1["red"] == self.init_red + 1

    def test_increment_resource_false(self):
        assert self.new_player.increment_card_resource("c4", "red", 1) is False
        assert self.no_change() is True

    def test_increment_card_resource_error(self):
        with self.assertRaises(KeyError):
            self.new_player.increment_card_resource("c1", "c2", 1)
        assert self.no_change() is True

    def test_validate_contribution_true(self):
        assert self.new_player.validate_contribution("c1", True, "red", 1) is True

    def test_validate_contribution_error_card(self):
        with self.assertRaises(KeyError):
            self.new_player.validate_contribution("c4", True, "red", 1)

    def test_validate_contribution_error_bool(self):
        with self.assertRaises(TypeError):
            self.new_player.validate_contribution("c1", "c2", "red", 1)

    def test_validate_contribution_error_colour(self):
        with self.assertRaises(NotColourError):
            self.new_player.validate_contribution("c1", True, "Red", 1)

    def test_validate_contribution_error_zero(self):
        with self.assertRaises(ZeroError):
            self.new_player.validate_contribution("c1", True, "red", 0)

    def test_validate_contribution_error_int(self):
        with self.assertRaises(ZeroError):
            self.new_player.validate_contribution("c1", True, "red", "blue")

    def test_change_contributions_error_card(self):
        with self.assertRaises(KeyError):
            self.new_player.change_contributions("c4", True, "red", 1)
        assert self.no_change() is True

    def test_change_contributions_error_bool(self):
        with self.assertRaises(TypeError):
            self.new_player.change_contributions("c1", "c2", "red", 1)
        assert self.no_change() is True

    def test_change_contributions_error_colour(self):
        with self.assertRaises(NotColourError):
            self.new_player.change_contributions("c1", True, "Red", 1)
        assert self.no_change() is True

    def test_change_contributions_error_zero(self):
        with self.assertRaises(ZeroError):
            self.new_player.change_contributions("c1", True, "red", 0)
        assert self.no_change() is True

    def test_change_contributions_error_int(self):
        with self.assertRaises(ZeroError):
            self.new_player.change_contributions("c1", True, "red", "blue")
        assert self.no_change() is True

    def test_change_contributions_false_resource(self):
        assert self.new_player.change_contributions("c1", True, "blue", 1) is False
        assert self.no_change() is True

    def test_change_contributions_fail_contribution(self):
        assert self.new_player.change_contributions("c2", True, "red", -1) is False
        assert self.no_change() is True

    def test_change_contributions_true_for_change(self):
        assert self.new_player.change_contributions("c1", True, "red", 1) is True
        assert self.new_player.c1["for"] is True
        assert self.new_player.c1["red"] is self.init_red + 1
        assert self.new_player.resources["red"] == self.init_red - 1

    def test_contribution_change_false_new_vote_neg(self):
        assert self.new_player.change_contributions("c3", not self.init_c3_for, "red", -1)
        assert self.no_change() is True

    def test_change_contributions_true_for_stay(self):
        assert self.new_player.change_contributions("c2", self.init_c2_for, "red", 1) is True
        assert self.new_player.c2["for"] == self.init_c2_for
        assert self.new_player.c2["red"] == self.init_c2c3_colour + 1
        assert self.new_player.resources["red"] == self.init_red - 1


if __name__ == "__main__":
    unittest.main()
