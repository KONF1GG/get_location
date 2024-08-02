import requests
import json
from bs4 import BeautifulSoup
import geocode as geocode
import functions
import time
import logging
from Yandex_map_parser import YandexMapParser
from tqdm import tqdm

url = "https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds%20%27@cityId:[10207%2010207]%20@searchType:{house}%27%20Limit%200%2010000&pretty=1"

response = requests.get(url)

logging.basicConfig(filename='coordinates.log', level=logging.INFO, format='%(message)s')

parser = YandexMapParser()

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
                for i, (key, value) in tqdm(enumerate(data.items(), start=1)):

                    settlementId = value.get('settlementId')
                    location = value.get('location', [])
                    if not location and settlementId == None:
                        uuid = value.get('UUID')
                        address_for_NominAPI = functions.clean_address(value.get('searchTitle'))
                        address_for_Yandex = functions.modify_address_for_Yandex(value.get('searchTitle'))
                        house_id = value.get('id')
                        address_checked_in_past = functions.check_if_house_in_bd(house_id=house_id)
                        house_number = value.get('name')
                        if house_number == '' or address_checked_in_past:
                            continue
                        print(f'{functions.clean_address(address_for_NominAPI)}')

                        location_from_NominAPI = geocode.get_location(address_for_NominAPI)

                        if not location_from_NominAPI:
                            location_from_Yandex = parser.get_location_from_Yandex(address_for_Yandex)

                            if not location_from_Yandex or not location_from_Yandex['latitude'] or not functions.check_address_correct(location_from_Yandex['Yandex_address'], house_number):
                                functions.add_address_without_location_in_DB(house_id=house_id, address=address_for_Yandex)
                            else:
                                try:
                                    functions.post_coordinates(uuid, location_from_Yandex['latitude'], location_from_Yandex['longitude'])
                                    yandex_counter += 1
                                    logging.info(f"YANDEX {yandex_counter}")
                                    logging.info(f"{location_from_Yandex} - LOCATION FROM YANDEX")
                                except Exception as e:
                                    print(f'Faild to post coordinates: {e}')
                                print(f'{location_from_Yandex} - LOCATION FROM YANDEX')


                        else:
                            try:
                                functions.post_coordinates(uuid, location_from_NominAPI[0], location_from_NominAPI[1])
                                nomin_counter += 1
                                logging.info(f"NOMI {nomin_counter}")
                                logging.info(f"{location_from_NominAPI} - LOCATION FROM NOMI")
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


