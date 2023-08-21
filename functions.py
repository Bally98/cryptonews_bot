import pymongo
import json
import base64
import os
import requests
import random
import pandas as pd
from tqdm import tqdm
from lxml import etree
from datetime import datetime, timedelta, timezone
def push_post(title, text_all, img):

    with open('client.json') as file:
        data = json.load(file)

    url = data['platform_url']
    user = data['platform_user']
    password = data['platform_password']
    type_status = data['type_status']
    category = data['category_id']
    # category = '121'

    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8')}

    image_path = 'pics/generated_preview.jpg'

    with open(image_path, 'rb') as image_file:
        encoded_img = base64.b64encode(image_file.read()).decode('utf-8')

    post = {
        'title': title,
        'status': f'{type_status}',  # тип
        'content': text_all,
        'categories': category,  # category ID
        'meta': {'_knawatfibu_url': 'data:image/jpeg;base64,'+ encoded_img}
    }

    response = requests.post(url, headers=header, json=post)

    if response.status_code == 200 or 201:
        print("Posted")
    else:
        print(f'Error. Status code: {response.status_code}')


def create_text(format_texts):

    with open("text.json", encoding='utf-8') as file:
        text = json.load(file)

    main_text = ''

    if format_texts == 'title':
        if len(text['title']) > 1:
            main_text = text["title"][f"{random.randint(1, len(text['title']))}"]
        else:
            main_text = text["title"]['1']
    else:
        for find_parts in range(len(text) - 1):
            title = text[f"{find_parts}"]["title"]
            main_parts = text[f"{find_parts}"]["main_text"]

            variable_text = ''
            variable_title = ''

            for find_count_parts in range(len(main_parts)):
                if main_parts[f"{find_count_parts}"] != '':
                    if len(main_parts) == 1:
                        variable_text += main_parts[f"{find_count_parts}"]
                    else:
                        variable_text += main_parts[f"{1, random.randint(len(main_parts[find_count_parts]))}"]

            if title != "":
                if len(title) == 1:
                    variable_title = title["0"]
                else:
                    variable_title = title[f"{random.randint(1, len(title))}"]

            main_text += variable_title + variable_text

    return main_text


def fetch_news(interval):
    today = datetime.today()
    if today.weekday() == 5 or today.weekday() == 6:
        print("It's the weekend. Stopping the code.")
        return pd.DataFrame.from_dict({})

    resources = pd.read_csv("newsfeeds.csv")
    resources = resources[resources['label'] == 'crypto']
    resources = resources[resources['format'] == 'website']

    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(hours=interval)

    news_list = []
    for index, row in tqdm(resources.iterrows(), total=resources.shape[0]):
        feed_url = row['feeds']
        source_name = row['name']  # Assuming the name column is present i

        if not feed_url:
            continue

        response = requests.get(feed_url)
        root = etree.fromstring(response.content)

        for entry in root.xpath('//item'):
            pub_date_str = entry.xpath('pubDate')[0].text
            try:
                pub_date = datetime.strptime(pub_date_str, '%a, %d %b %Y %H:%M:%S %z')
            except ValueError:
                try:
                    pub_date = datetime.strptime(pub_date_str, '%d/%m/%Y %H:%M:%S.%f')
                except ValueError:
                    continue
            pub_date = pub_date.astimezone(timezone.utc)

            if yesterday <= pub_date <= now:
                headline = entry.xpath('title')[0].text
                link = entry.xpath('link')[0].text
                news_dict = {'pub_date': pub_date, 'headline': headline, 'link': link, 'source_name': source_name}
                news_list.append(news_dict)

    df = pd.DataFrame.from_dict(news_list)
    return df


def filter_by_keywords(feed_df, keyword):
    feed_df['contains'] = False
    for k in keyword:
        feed_df['contains'] += feed_df['headline'].str.lower().str.contains(k)
    return feed_df[feed_df['contains']]


def format_fetched_news(df, top_n):
    df = df.sample(frac=1).reset_index(drop=True)
    df = df[:top_n]
    res = []
    for index, row in df.iterrows():
        headline_with_source = [row['headline'], row['source_name']]
        res.append("<li><a href={0}>{1[0]}</a> [{1[1]}]</li>".format(row['link'], headline_with_source))
    return res


def fetch_crypto_news(keywords, top_n, interval=24):
    raw_rss = fetch_news(interval)
    filtered = filter_by_keywords(raw_rss, keywords)
    result = format_fetched_news(filtered, top_n)
    return result