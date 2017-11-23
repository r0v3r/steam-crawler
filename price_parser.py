from HTMLParser import HTMLParser
import re

class PriceParser(HTMLParser):
    # set text of HTML tag in price field
    # price <div> may contain several prices,
    # the last price is the current price
    def handle_data(self, data):
        # use reg to match int value
        tmp = re.findall(r'\d+', data.encode('utf-8'),0)
        if len(tmp)>0:
            self.price =int(tmp[0])