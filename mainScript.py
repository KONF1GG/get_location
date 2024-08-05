import requests
import json
from bs4 import BeautifulSoup
import geocode as geocode
import functions
import time
import logging
from Yandex_map_parser import YandexMapParser
from tqdm import tqdm

parser = YandexMapParser()
YandexMap_broken = False
time.sleep(5)

for limit_start in tqdm(['10000', '20000', '30000', '40000', '50000', '60000', '70000', '80000']):
    limit_ = '10000'
    url = f'https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds:geo%20%27%20@searchType:%7Bhouse%7D%20@searchTitle:%D0%BC%D0%B0%D0%B3%D0%BD%D0%B8%D1%82%D0%BE%D0%B3%D0%BE%D1%80%D1%81%D0%BA%20-@latitude:[0%2090]%27%20Limit%20{limit_start}%20{limit_}&pretty=1&pretty=1'

    response = requests.get(url)

    logging.basicConfig(filename='coordinates.log', level=logging.INFO, format='%(message)s')

    yandex_counter = 0
    nomin_counter = 0
    count = 1

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
                        # print(location)
                        # print(settlementId)
                        if settlementId == None:
                            uuid = value.get('UUID')
                            address_for_NominAPI = functions.clean_address(value.get('searchTitle'))
                            address_for_Yandex = functions.modify_address_for_Yandex(value.get('searchTitle'))
                            house_id = value.get('id')
                            address_checked_in_past = functions.check_if_house_in_bad_bd(house_id=house_id)
                            address_added_in_past = functions.check_if_address_in_bd(house_id=house_id)
                            house_number = value.get('name')
                            if house_number == '' or address_checked_in_past:
                                print('BadAddress')
                                continue
                            if address_added_in_past:
                                print('AddedBefore')
                                continue
                            print(f'{functions.clean_address(address_for_NominAPI)}')

                            location_from_NominAPI = geocode.get_location(address_for_NominAPI)

                            if not location_from_NominAPI:
                                if not YandexMap_broken:

                                    time.sleep(5)
                                    location_from_Yandex = parser.get_location_from_Yandex(address_for_Yandex)
                                    if location_from_Yandex['Input_not_found'] == True:
                                        YandexMap_broken = True

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
                                    continue
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
                            print('it is a settlement')

            else:
                print("No <pre> tag found in the response content")

        except json.JSONDecodeError as e:
            print("Failed to decode JSON. The server response might not be in JSON format.")
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")


