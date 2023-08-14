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

background = Image.open("background_crypto.jpg")

title_text = 'The biggest cryptos of the last 24h'
coin_text = 'SOL'
exchange_text = 'Binance'
percent_text = '28.5%'
date_text = 'August 14 2023'

font_title = ImageFont.truetype('days2.ttf', size=70)
font_coin = ImageFont.truetype('days2.ttf', size=70)
font_exchange = ImageFont.truetype('days2.ttf', size=60)
font_percent = ImageFont.truetype('days2.ttf', size=90)
font_date = ImageFont.truetype('days2.ttf', size=30)


title = ImageDraw.Draw(background)
title.text((960, 250), title_text, anchor='ms', font=font_title, fill='white')

coin = ImageDraw.Draw(background)
coin.text((780, 600), coin_text, anchor='ms', font=font_coin, fill='white')

exchange = ImageDraw.Draw(background)
exchange.text((965, 430), exchange_text, anchor='ms', font=font_exchange, fill='white')

percent = ImageDraw.Draw(background)
percent.text((1050, 600), percent_text, anchor='ms', font=font_percent, fill='white')

date = ImageDraw.Draw(background)
date.text((965, 950), date_text, anchor='ms', font=font_date, fill='white')



background.save('back2.jpg')

