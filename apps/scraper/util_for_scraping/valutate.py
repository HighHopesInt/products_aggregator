import json
from urllib.request import urlopen


def get_current_usd():
    response = urlopen('https://www.cbr-xml-daily.ru/daily_json.js').read() \
        .decode('utf-8')
    response_json = json.loads(response)
    return response_json['Valute']['USD']['Value']
