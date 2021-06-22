import re
import requests


class StockParser:
    pattern = re.compile(r'/stock=.*')
    separator = '='

    def parse(self, message):
        """
        Returns the stock code of message if found or None
        """
        result = self.pattern.match(message)
        if result:
            return message.split(self.separator)[1]
        return None


class StockService:
    url = 'https://stooq.com/q/l/?s={code}&f=sd2t2ohlcv&h&e=csv'

    def get_stock_data(self, code):
        """
        Returns stock data in a list with the following structure:
        [Symbol, Date, Time, Open, High, Low, Close, Volume]
        """
        response = requests.get(self.url.format(code=code))
        return response.text.split('\n')[1].strip().split(',')


class StockBot:
    def __init__(self):
        self.parser = StockParser()
        self.service = StockService()
    
    def process_message(self, message):
        code = self.parser.parse(message)
        if code:
            stock_data = self.service.get_stock_data(code)
            symbol, amount_per_share = stock_data[0], stock_data[6]
            if amount_per_share == 'N/D':
                return f'No info found for {symbol}'
            return f'{symbol} quote is ${amount_per_share} per share'
