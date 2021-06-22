import unittest

from bot import StockParser


class TestParser(unittest.TestCase):
    parser = StockParser()
    
    def test_common_string(self):
        result = self.parser.parse('This is a test string')
        self.assertIsNone(result)
    
    def test_begin_slash_string(self):
        result = self.parser.parse('/This is a test string')
        self.assertIsNone(result)
    
    def test_up_to_separator(self):
        result = self.parser.parse('/stock=')
        self.assertEqual(result, '')
    
    def test_full_match(self):
        result = self.parser.parse('/stock=aapl.us')
        self.assertEqual(result, 'aapl.us')


if __name__ == '__main__':
    unittest.main()