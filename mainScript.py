import requests
import json
from bs4 import BeautifulSoup
import geocode as geocode
import parser
import functions
import time
import logging

# url = "https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds%20%27@settlementId:[10193%2010193]%20@searchType:{house}%27%20Limit%201000%205000&pretty=1"
url = "https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds%20%27@settlementId:[10193%2010193]%20@searchType:{house}%27%20Limit%201000%205000&pretty=1"

response = requests.get(url)

logging.basicConfig(filename='coordinates.log', level=logging.INFO, format='%(message)s')


yandex_counter = 0
nomin_counter = 0

if response.status_code == 200:
    try:
        soup = BeautifulSoup(response.text, 'html.parser')

        pre_tag = soup.find('pre')
        if pre_tag:
            json_text = pre_tag.text
            data = json.loads(json_text)

            if not data:
                print("No data returned from the server.")
            else:
                for i, (key, value) in enumerate(data.items(), start=1):
                    
                    uuid = value.get('UUID')
                    address_for_NominAPI = functions.clean_address(value.get('addressShort'))
                    address_for_Yandex = value.get('title')  
                    location = value.get('location', [])
                    house_number = value.get('rbtName')
                    print(f'{address_for_NominAPI} - ADDRESS') 

                    if not location:
                        location_from_NominAPI = geocode.get_location(address_for_NominAPI)
                        if not location_from_NominAPI:
                            # time.sleep(60)
                            location_from_Yandex = parser.get_location_from_Yandex(address_for_Yandex)
                            if location_from_Yandex:
                                if not location_from_Yandex['latitude'] or not functions.check_address_correct(location_from_Yandex['Yandex_address'], house_number):
                                    print('There is no location of this address')
                                else:
                                    try:
                                        functions.post_coordinates(uuid, location_from_Yandex['latitude'], location_from_Yandex['longitude'])
                                        yandex_counter += 1
                                        logging.info(f"Яндекс {yandex_counter}")
                                        # logging.info(f"{location_from_Yandex} - LOCATION FROM YANDEX")
                                    except Exception as e:
                                        print(f'Faild to post coordinates: {e}')
                                    print(f'{location_from_Yandex} - LOCATION FROM YANDEX')
                        else:
                            try:
                                functions.post_coordinates(uuid, location_from_NominAPI[0], location_from_NominAPI[1])
                                logging.info(f"Сайт {nomin_counter}")
                                # logging.info(f"{location_from_NominAPI} - LOCATION FROM NOMI")
                            except Exception as e:
                                print(f'Faild to post coordinates: {e}')
                            print(f'{location_from_NominAPI} - LOCATION FROM NOMI')
                    else:
                        print('Location already exists')

        else:
            print("No <pre> tag found in the response content")

    except json.JSONDecodeError as e:
        print("Failed to decode JSON. The server response might not be in JSON format.")
else:
    print(f"Failed to fetch data. Status code: {response.status_code}")


