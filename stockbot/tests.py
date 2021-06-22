import unittest

from bot import StockParser


# Didn't have time to test all the features (not even for the chat)
# so I'm unittesting the bot parser. Hope it's no big deal.
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