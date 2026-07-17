import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Game import Game


class GameSaveLoadTests(unittest.TestCase):
    def test_save_and_load_round_trip(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            save_path = Path(tmpdir) / "game_save.json"
            game = Game(save_file=save_path)
            game.player_hp = 77
            game.damage = 30
            game.has_knife = True
            game.has_medkit = True
            game.has_shield = True
            game.inventory = ["ніж", "аптечка"]

            game.save_game()
            self.assertTrue(save_path.exists())

            reloaded = Game(save_file=save_path)
            self.assertEqual(reloaded.player_hp, 77)
            self.assertEqual(reloaded.damage, 30)
            self.assertTrue(reloaded.has_knife)
            self.assertTrue(reloaded.has_medkit)
            self.assertTrue(reloaded.has_shield)
            self.assertEqual(reloaded.inventory, ["ніж", "аптечка"])


if __name__ == "__main__":
    unittest.main()
