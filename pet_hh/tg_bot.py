import parcing  # Сбор данных с HeadHunter
import requests
import os
from datetime import date
from urllib.parse import urlencode

chat_id = 492659501  # Находим по https://api.telegram.org/bot{token}/getUpdates
bot_id = 6393402102  # Находим по https://api.telegram.org/bot{token}/getMe

# Токен для подключения
token = os.environ.get('PET_HH_TG_TOKEN')

print(token)
def send_message(chat_id,token,text):
    # Отправка сообщения:
    # text - текст сообщения
    url = f'https://api.telegram.org/bot{token}/sendMessage?'
    params = {'chat_id': chat_id, 'text':text}
    print('Message:',requests.get(url,params))

def send_document(chat_id,token,document,caption):
    # Отправка файла:
    # document - локальный путь до файла
    # caption - сообщение с файлом
    url = f'https://api.telegram.org/bot{token}/sendDocument?'
    params = {'chat_id': chat_id, 'caption':caption}
    with open(document, 'rb') as f:
        files = {'document':f}
        print('Document:',requests.post(url,params,files=files))

# Отправка сообщения и файла:
today_date = date.today().strftime("%d %B %Y")

# send_message(text=f'Отчёт на {today_date} готов!'
#              ,chat_id =chat_id
#              ,token=token)

send_document(chat_id =chat_id,
              token=token,
              document='boss.png',
              caption=f'Отчёт на {today_date} готов!')

