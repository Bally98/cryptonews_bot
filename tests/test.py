import pandas as pd
from tqdm import tqdm
from datetime import datetime, timedelta, timezone
import plotly.express as px
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import calendar, time
from datetime import datetime, timedelta
import datetime
import json
import os
import requests

from time import sleep


def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

background = Image.open("pics/Banner.jpg")
img_width, img_height = background.size

coin_text = 'PAXG'
exchange_text = 'OKEX'
percent_text = '109.1%'
date_text = 'May 16 2023'

font_coin = ImageFont.truetype('Martian Fonts - Martian Grotesk UWd Md.ttf', size=50)
font_exchange = ImageFont.truetype('Martian Fonts - Martian Grotesk XWd XBd.ttf', size=30)
font_percent = ImageFont.truetype('Martian Fonts - Martian Grotesk Nr Th.ttf', size=110)
font_date = ImageFont.truetype('Exo-Bold.ttf', size=25)


coin_text_width, coin_text_height = get_text_dimensions(coin_text, font_coin)
coordinat_coin = img_width - coin_text_width - 480
coin = ImageDraw.Draw(background)
coin.text((coordinat_coin, 250), coin_text, font=font_coin, fill='white')


percent_text_width,percent_text_height = get_text_dimensions(percent_text, font_percent)
coordinat_percent = img_width - percent_text_width - 480
percent = ImageDraw.Draw(background)
percent.text((coordinat_percent, 310), percent_text, font=font_percent, fill='white')

exchange_text_width,exchange_text_height = get_text_dimensions(exchange_text, font_exchange)
coordinat_exchange = img_width - exchange_text_width - 480
exchange = ImageDraw.Draw(background)
exchange.text((coordinat_exchange, 460), exchange_text, font=font_exchange, fill='white')

date = ImageDraw.Draw(background)
date.text((50, 730), date_text, font=font_date, fill='white', align='left')



# print(img_width)
background.show()
# slogan = ImageDraw.Draw(background)
# slogan.text((coordinat_slogan, 1150), slogan_text,  font=font_slogan, fill='white', align='right')

# # Получите размеры изображения
# ширина_изображения, высота_изображения = image.size
#
# # Получите размеры текста
# ширина_текста, высота_текста = draw.textsize(текст, font=font)
#
# # Рассчитайте координату X для выравнивания по правому краю
# x = ширина_изображения - ширина_текста - 10  # 10 - отступ от правого края
#
# # Добавьте текст на изображение с выравниванием по правому краю
# draw.text((x, 10), текст, font=font, fill=(255, 255, 255))
#
# # Сохраните изображение с добавленным текстом
# image.save('путь_к_сохраненному_изображению/новое_имя_изображения.jpg')  # Замените на нужный путь и имя