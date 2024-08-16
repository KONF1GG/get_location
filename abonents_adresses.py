import requests
import json
from bs4 import BeautifulSoup
import functions
import time
from Yandex_map_parser import YandexMapParser
from tqdm import tqdm
import pandas as pd

file = pd.read_csv('АбонентскиеАдресабезКоординат.csv', delimiter=';', encoding='windows-1251')
#
# parser = YandexMapParser()
# time.sleep(5)
YandexMap_broken = False
setl_list = functions.get_settlements()
list_of_abonents_id = ['707822']

# for house_id in file.houseId:
#     list_of_abonents_id.append(house_id)


# count_b = 0
# count_a = 0
# count_o = 0
#
# for house in tqdm(list_of_abonents_id):
#     if functions.check_if_house_in_bad_bd(house):
#         count_b += 1
#     elif functions.check_if_address_in_bd(house):
#         count_a += 1
#     else:
#         count_o += 1
#         print(house)
# print('bad: ', count_b)
# print('add:', count_a)
# print('o:', count_o)

# for setl in tqdm(setl_list):
#     for limit_start in(
#             ['0', '10000', '20000', '30000', '40000', '50000', '60000', '70000', '80000', '90000', '100000']):
#         limit_ = '10000'
#         url = f'https://ws.freedom1.ru/redis/raw?query=FT.SEARCH%20idx:adds:geo%20%27%20@searchType:%7Bhouse%7D%20@searchTitle:{setl}%27%20Limit%20{limit_start}%20{limit_}&pretty=1'
#
#         response = requests.get(url)
#
#         if response.status_code == 200:
#             try:
#                 soup = BeautifulSoup(response.text, 'html.parser')
#
#                 pre_tag = soup.find('pre')
#                 if pre_tag:
#                     json_text = pre_tag.text
#                     data = json.loads(json_text)
#
#                     if not data:
#                         print("No data returned from the server.")
#                     else:
#                         for i, (key, value) in enumerate(data.items(), start=1):
#
#
#                             house_id = value.get('id')
#                             if house_id not in list_of_abonents_id:
#                                 continue
#
#                             settlementId = value.get('settlementId')
#                             uuid = value.get('UUID')
#                             search_title = value.get('searchTitle')
#                             address_for_NominAPI = functions.clean_address(search_title)
#                             address_for_Yandex = functions.modify_address_for_Yandex(search_title)
#                             address_checked_in_past = functions.check_if_house_in_bad_bd(house_id=house_id)
#                             address_added_in_past = functions.check_if_address_in_bd(house_id=house_id)
#                             house_number = value.get('name')
#                             if house_number == '':
#                                 functions.add_address_without_location_in_DB(house_id=house_id,
#                                                                              address=address_for_Yandex)
#                                 continue
#                             if address_checked_in_past:
#                                 # print('BadAddress')
#                                 # print(house_id)
#                                 continue
#                             if address_added_in_past:
#                                 # print('AddedBefore')
#                                 # print(house_id)
#                                 continue
#                             print(f'{functions.clean_address(address_for_NominAPI)}')
#
#                             location_from_NominAPI = functions.get_location(address_for_NominAPI)
#
#                             if not location_from_NominAPI:
#                                 if not YandexMap_broken:
#                                     location_from_Yandex = parser.get_location_from_Yandex(address_for_Yandex)
#                                     if location_from_Yandex is not None:
#                                         if location_from_Yandex['Input_not_found'] == True:
#                                             YandexMap_broken = True
#
#                                     if not location_from_Yandex or not location_from_Yandex[
#                                         'latitude'] or not functions.check_address_correct(
#                                             location_from_Yandex['Yandex_address'], house_number):
#                                         functions.add_address_without_location_in_DB(house_id=house_id,
#                                                                                      address=address_for_Yandex)
#                                     else:
#                                         try:
#                                             functions.post_coordinates(uuid, location_from_Yandex['latitude'],
#                                                                        location_from_Yandex['longitude'])
#                                             functions.post_address_in_bd(house_id, address_for_NominAPI,
#                                                                          [location_from_Yandex['latitude'],
#                                                                           location_from_Yandex['longitude']])
#                                         except Exception as e:
#                                             print(f'Faild to post coordinates: {e}')
#                                         print(f'{location_from_Yandex} - LOCATION FROM YANDEX')
#                                 else:
#                                     continue
#                             else:
#                                 try:
#                                     functions.post_coordinates(uuid, location_from_NominAPI[0],
#                                                                location_from_NominAPI[1])
#                                     functions.post_address_in_bd(house_id, address_for_NominAPI,
#                                                                  location_from_NominAPI)
#                                 except Exception as e:
#                                     print(f'Faild to post coordinates: {e}')
#                                 print(f'{location_from_NominAPI} - LOCATION FROM NOMI')
#
#                 else:
#                     print("No <pre> tag found in the response content")
#
#             except json.JSONDecodeError as e:
#                 print("Failed to decode JSON. The server response might not be in JSON format.")
#         else:
#             print(f"Failed to fetch data. Status code: {response.status_code}")
#
#
