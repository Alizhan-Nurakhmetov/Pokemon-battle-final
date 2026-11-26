import unittest
from battle import play
from moves import damage
from game import trainer_name

class BattleTests(unittest.TestCase):
    def test_trainer_name_rejects_punctuation(self):
        """Reject punctuation in trainer names"""
        with self.assertRaises(ValueError):
                trainer_name("!!")

