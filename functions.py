import pymongo
import json
import base64
import os
import requests
import random
def push_post(title, text_all):

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

    post = {
        'title': title,
        'status': f'{type_status}',  # тип
        'content': text_all,
        'categories': category, # category ID
    }

    response = requests.post(url, headers=header, json=post).json()

    print("Posted")


def create_text(format_texts):

    with open("en_text.json", encoding='utf-8') as file:
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
