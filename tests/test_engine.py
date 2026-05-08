import unittest
from src.core.engine import InterpretiveEngine

class TestEngine(unittest.TestCase):
    def test_init(self):
        engine = InterpretiveEngine()
        self.assertIsNotNone(engine)
