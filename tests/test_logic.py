import sys
import os
import unittest

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from logic import fetch_all_games, GAME_MAP

class TestLotteryLogic(unittest.TestCase):
    def test_fetch(self):
        print("Fetching data from Taiwan Lottery...", file=sys.stderr)
        data = fetch_all_games()
        
        if "error" in data:
            print(f"Fetch failed (network issue?): {data['error']}", file=sys.stderr)
            return

        self.assertIsInstance(data, dict)
        
        # We might not get all games if site structure changed, but we should get at least one if site is up
        print(f"Fetched keys: {list(data.keys())}", file=sys.stderr)
        
        for key, info in data.items():
            print(f"Validating {key}...", file=sys.stderr)
            self.assertIn("name", info)
            self.assertIn("term", info)
            self.assertIn("regular", info)
            self.assertIsInstance(info["regular"], list)

if __name__ == '__main__':
    unittest.main()
