import requests
from bs4 import BeautifulSoup
import json
from tqdm import tqdm
import re

def modify_address(address):
    if 'сад' in address:
        address = address.replace('сад', '')

    address = address.replace('  ', ' ')

    address = re.sub(r'(?<=\d) n | n(?=\d)', '-', address)
    address = re.sub(r'\d-(?=\d)', '', address)
    return address.strip()


url = "https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds%20%27@cityId:[10207%2010207]%20@searchType:{house}%27%20Limit%2050%20500&pretty=1"

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

pre_tag = soup.find('pre')

if pre_tag:
    json_text = pre_tag.text
    data = json.loads(json_text)

    if not data:
        print("No data returned from the server.")
    else:
        for i, (key, value) in tqdm(enumerate(data.items(), start=1)):

            settlementId = value.get('settlementId')
            location = value.get('location', [])
            if not location and settlementId == None:
                address_for_Yandex = value.get('searchTitle')
                print(modify_address(address_for_Yandex))


