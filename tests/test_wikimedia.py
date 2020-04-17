import unittest
import logging
from pathlib import Path
import src.config

DATA_FOLDER = Path(__file__).parent / 'data'

logging.basicConfig(level=logging.INFO)


class TestIndex(unittest.TestCase):
    print(src.config.ROOT)
    # breakpoint()


if __name__ == '__main__':
    unittest.main()

TestIndex()
