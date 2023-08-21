import pandas as pd
import requests
from tqdm import tqdm
from lxml import etree
from datetime import datetime, timedelta, timezone



url = 'ссылка_на_обработчик'  # Замените на URL сервера обработки запросов

headers = {
    'Content-Type': 'application/json',
    # Добавьте другие заголовки, если необходимо
}

data = {
    'meta': {'_knawatfibu_': 'ссылка_на_изображение'},
    # Другие данные
}

image_path = 'путь_к_изображению/имя_изображения.jpg'

with open(image_path, 'rb') as image_file:
    files = {'_knawatfibu_': image_file}

    response = requests.post(url, headers=headers, json=data, files=files)

print(response.text)

