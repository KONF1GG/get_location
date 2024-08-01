import re
import requests
from data import BD_AUTHORIZATION

# Функция для обработки адресов
def clean_address(address):
    shortcuts = ['дом', 'респ', 'край', 'обл', 'гфз', 'аобл', 'аокр', 'мр-н', 'го', 'гп', 'сп', 'внр-н', 'внтерг', 'пос', 'р-н', 'с/с', 'г', 'пгт', 'рп', 'кп', 'гп', 'п', 'аал', 'арбан', 'аул',
    'в-ки', 'г-к', 'з-ка', 'п-к', 'киш', 'п_ст', 'п_ж/д_ст', 'ж/д_бл-ст', 'ж/д_б-ка', 'ж/д_в-ка', 'ж/д_к-ма', 'ж/д_к-т', 'ж/д_пл-ма', 'ж/д_пл-ка', 'ж/д_пп', 'ж/д_оп', 
    'ж/д_рзд', 'ж/д_ст', 'м-ко', 'д', 'с', 'сл', 'ст-ца', 'ст', 'у', 'х', 'рзд', 'зим', 'б-г', 'вал', 'ж/р', 'зона', 'кв-л', 'мкр', 'ост-в', 'парк', 'платф', 'п/р', 'р-н', 
    'сад', 'сквер', 'тер', 'тер_СНО', 'тер_ОНО', 'тер_ДНО', 'тер_СНТ', 'тер_ОНТ', 'тер_ДНТ', 'тер_СПК', 'тер_ОПК', 'тер_ДПК', 'тер_СНП', 'тер_ОНП', 'тер_ДНП', 'тер_ТСН', 
    'тер_ГСК', 'ус', 'терфх', 'ю', 'ал', 'б-р', 'взв', 'взд', 'дор', 'ззд', 'км', 'к-цо', 'коса', 'лн', 'мгстр', 'наб', 'пер-д', 'пер', 'пл-ка', 'пл', 'пр-д', 'пр-к', 
    'пр-ка', 'пр-лок', 'пр-кт', 'проул', 'рзд', 'ряд', 'с-р', 'с-к', 'сзд', 'тракт', 'туп', 'ш', 'влд', 'г-ж', 'д', 'двлд', 'зд', 'з/у', 'кв', 'ком', 'подв', 'кот', 
    'п-б', 'к', 'ОНС', 'офис', 'пав', 'помещ', 'рабуч', 'скл', 'coop', 'стр', 'торгзал', 'цех'
]

# Объединяем сокращения в одно регулярное выражение
    shortcuts_regex = r'\b(?:' + '|'.join(map(re.escape, shortcuts)) + r')\b'

    # Удаляем сокращения из адреса
    address = re.sub(shortcuts_regex, '', address)
    # Убираем двойные пробелы и лишние пробелы по краям    address = re.sub(r'\s+', ' ', address).strip()
    
    return address

#Функция для проверки правильности найденного дома
def check_address_correct(address, house_number):
    house_number = re.sub(r'[\\]', '', house_number)
    cleaned_house_number = re.sub(r'[\\/]', '', house_number)
    if house_number == address.split()[-1] or cleaned_house_number == address.split()[-1]:
        return True
    else:
        return False
    
#Функция для заполнения БД координатами
def post_coordinates(uuid, latitude, longitude):
    # test bd
    # url = 'http://dev1c.freedom1.ru/UNF_TEST_WS2/hs/apps/setHomeCoordinates'
    # main bd
    url = 'https://support.freedom1.ru/UNF_CRM_WS/hs/setHomeCoordinates'
    headers = {
        'Authorization': BD_AUTHORIZATION,
        'Content-Type': 'application/json'
    }
    
    data = {
        "UUID": uuid,
        "latitude": latitude,
        "longitude": longitude
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        print("Координаты успешно отправлены!")
    else:
        print(f"Ошибка при отправке координат: {response.status_code} - {response.text}")

def modify_address_for_Yandex(address):
    if 'сад' in address:
        address = address.replace('сад', '')

    address = address.replace('  ', ' ')

    address = re.sub(r'(?<=\d) n | n(?=\d)', '-', address)
    address = re.sub(r'\d-(?=\d)', '', address)
    return address.strip()



# uuid = "c3d566d8-9f3d-11e5-a904-3085a9f76558"
# latitude = 53.290460
# longitude = 59.135718

# post_coordinates(uuid, latitude, longitude)
# # Список адресов
# addresses = [
#     "Агаповский р-н Агаповка Горная 8",
#     "Агаповский р-н Агаповка Неженка-2 сад 43",
#     "Агаповский р-н Агаповка Мелиоратор сад 222"
# ]

# # Очистка адресов
# cleaned_addresses = [clean_address(address) for address in addresses]

# # Вывод очищенных адресов
# for address in cleaned_addresses:
#     print(address)


# address = 'село Агаповка 1A'
# house_number = '1/A'
# print(check_address_correct(address, house_number))

# Список адресов для теста
# addresses = [
#     "Агаповский р-н Агаповка 60 лет Октября 22/1",
#     "Голубицкая ст-ца Набережная ул 39",
#     "Карский х Длинная ул 126",
#     "Агаповский Гумбейка ж/д_ст Заводская 3"
# ]

# # Применение функции ко всем адресам
# for address in addresses:
#     print(clean_address(address))