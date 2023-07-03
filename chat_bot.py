import requests
import time
import pprint

TOKEN = '5871677585:AAFLrb03ZuFRlsq3cnOQ_Dplq3DRRJ7j_EA'

BOT_URL = f'https://api.telegram.org/bot{TOKEN}'

proxies = {
    'http': '221.141.158.183:80',
    'https': '117.251.103.186:8080',
}

url = f'{BOT_URL}/getMe'
result = requests.get(url, proxies=proxies)

#print(result.text)
url_1 = f'{BOT_URL}/getUpdates'
while True:
    time.sleep(3)
    result = requests.get(url_1, proxies=proxies)
    pprint.pprint(result.json())
    messages = result.json()['result']
    for message in messages:
        chat_id = message['message']['chat']['id']
        url_send = f'{BOT_URL}/sendMessage'
        params = {
                'chat_id': chat_id,
                'text': 'Здравствуйте!'
                  }
        answer = requests.post(url_send, params=params, proxies=proxies)