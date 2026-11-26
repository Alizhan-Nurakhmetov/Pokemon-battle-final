import unittest
from battle import play
from moves import damage
from game import trainer_name

class BattleTests(unittest.TestCase):
    def test_trainer_name_rejects_punctuation(self):
        """Reject punctuation in trainer names"""
        with self.assertRaises(ValueError):
                trainer_name("!!")

    def test_basic_and_type_damage(self):
        """Check damage for each matchup"""
        grass = {"type": "grass"}
        water = {"type": "water"}
        self.assertEqual(damage("Basic", grass, water), 10)
        self.assertEqual(damage("Type", grass, water), 16)
        self.assertEqual(damage("Type", water, grass), 6)

    def test_knockout_stops_the_turn(self):
        player = {"name": "Bulbasaur", "type": "grass"}
        rival = {"name": "Squirtle", "type": "water"}
        battle = {"fighters": [player, rival], "hp": [45, 5]}
        updated, message = play(battle, "Basic")
        self.assertEqual(updated["hp"], [45, 0])
        self.assertIn("You win!", message)
        with self.assertRaises(ValueError):
            play(updated, "Basic")
