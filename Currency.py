import requests
import json
import lxml.html
from lxml.html import etree
from io import StringIO, BytesIO
from config import key_cbr_or



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

print(get_rates())