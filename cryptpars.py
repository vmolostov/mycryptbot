import re
import requests
from bs4 import BeautifulSoup

URL = 'https://minfin.com.ua/currency/crypto/'
PARAMS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'
}


class Bot:

    def pretty_print(self, item):
        if '-' not in item['Изменение за день']:
            chg = '+' + item['Изменение за день']
        else:
            chg = item['Изменение за день']

        response = 'Currency: ' + item['Валюта'] + '\n\n' + 'Position in the rating: ' + item[
            '№'] + '\n\n' + 'Price, USD: ' + item['Цена, USD'] + '\n\n' + 'Market Cap, USD: ' + item[
                       'Капитализация, USD'] + '\n\n' + 'Chg (24H): ' + chg + '%'
        return response

    def list_of_crypt(self):
        list_of_crypt = []
        for item in self.crypto_parse():
            list_of_crypt.append(item['Валюта'])
        return list_of_crypt

    def crypto_parse(self):
        x = 1
        db = []
        while x <= 2:
            response = requests.get(URL + str(x), params=PARAMS)
            x += 1
            html = response.text
            if response.status_code == 200:
                soup = BeautifulSoup(html, 'html.parser')
                items = soup.find_all('div', class_='coin js-sort-elem')
                for item in items:
                    db.append({
                        '№': item.find('div', class_='coin-item').get_text(),
                        'Валюта': item.find('div', class_='coin-item coin-name row-nocollapsed').get('title'),
                        'Цена, USD': item.find('div', class_='coin-item coin-price row-nocollapsed').get(
                            'data-sort-val'),
                        'Капитализация, USD': item.find('div', class_='coin-item coin-capital row-collapsed').get(
                            'data-sort-val'),
                        'Изменение за день': item.find('div', class_='coin-item coin-changes row-collapsed').get(
                            'data-sort-val')
                    })
        return db

    def for_tg_bot(self, message):
        for item in self.crypto_parse():
            if re.search(message.title(), item['Валюта']):
                return self.pretty_print(item)
        return "I don't understand what currency information you want to request." + '\n' + "Try entering the name again!"


bot = Bot()
