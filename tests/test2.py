import pandas as pd
import requests
from tqdm import tqdm
from lxml import etree
from datetime import datetime, timedelta, timezone


def fetch_news(interval):
    today = datetime.today()
    if today.weekday() == 5 or today.weekday() == 6:
        print("It's the weekend. Stopping the code.")
        return pd.DataFrame.from_dict({})

    resources = pd.read_csv("")
    resources = resources[resources['label'] == 'crypto']
    resources = resources[resources['format'] == 'website']

    now = datetime.now(timezone.utc)
    yesterday = now - timedelta(hours=interval)

    news_list = []
    for index, row in tqdm(resources.iterrows(), total=resources.shape[0]):
        feed_url = row['feeds']
        source_name = row['name']  # Assuming the name column is present in

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
        headline_with_source = [f"{row['headline']}", f"{row['source_name']}"]
        # headline_with_source = f"{row['headline']} [{row['source_name']}]"
        res.append("<li><a href={0}>{1[0]}</a>{1[1]}</li>".format(row['link'], headline_with_source))
    return res


def fetch_crypto_news(keywords, top_n, interval=24):
    raw_rss = fetch_news(interval)
    filtered = filter_by_keywords(raw_rss, keywords)
    result = format_fetched_news(filtered, top_n)
    return result

print(fetch_crypto_news(['btc', 'eth'], 5))

