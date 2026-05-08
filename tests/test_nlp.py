import unittest
from src.nlp.extractor import SymbolExtractor

class TestNLP(unittest.TestCase):
    def test_extractor(self):
        extractor = SymbolExtractor()
        self.assertIsNotNone(extractor)
