import requests
import json
from lxml.html import etree
from io import BytesIO
from config import keys, key_cbr, key_cbr_or


class ConvertionException(Exception):
    pass


class Converter:

    @staticmethod
    def get_rates():
        cbr_rates = {}
        r = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        tree = etree.parse(BytesIO(r.content))
        root = tree.getroot()
        for code in key_cbr_or:
            f_str = f"./Valute[@ID =\'{key_cbr_or[code]}\']"
            elem = root.find(f"./Valute[@ID =\'{key_cbr_or[code]}\']")
            cbr_rates[code] = float((elem[4].text).replace(",", ".")) / int(elem[2].text)
        return cbr_rates

    @staticmethod
    def do_convert(quote: str, base: str, amount: str):
        rates = Converter.get_rates()
        if quote == base:
            raise ConvertionException(f"Невозможно перевести одинаковые валюты {base}.")
        if quote not in rates.keys() and quote != 'рубль':
            raise ConvertionException(f"Не удалось обработать валюту {quote}.")
        if base not in rates.keys() and base != 'рубль':
            raise ConvertionException(f"Не удалось обработать валюту {quote}.")
        try:
            amount = float(amount.replace(',', '.'))
        except ValueError:
            raise ConvertionException(f"Не удалось обработать количество {amount}.")

        #cbr = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
        #cbr_rates = json.loads(cbr.content)['Valute']

        if quote != 'рубль' and base != 'рубль':
            total_base = (rates[quote] / rates[base]) * amount
        elif base == 'рубль':
            total_base = rates[quote] * amount
        else:
            total_base = amount / rates[base]

        # r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        # total_base = json.loads(r.content)[base_ticker]*amount

        return total_base

    # def get_cbr_rates(self):
    #    cbr = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    #    return json.loads(cbr.content)
