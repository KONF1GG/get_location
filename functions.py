import re
import requests
import data

# Функция для обработки адресов
def clean_address(address):
    # Удаляем ненужные части адреса
    address = re.sub(r'р-н|сад', '', address).strip()
    # Регулярное выражение для извлечения города, улицы и номера дома
    match = re.search(r'(?P<city>\b\w+\b) (?P<street>[\w-]+\s[\w-]+) (?P<number>\d+)', address)
    if match:
        return f"{match.group('city').strip()} {match.group('street').strip()} {match.group('number')}"
    return address

#Функция для проверки правильности найденной улицы
def check_address_correct(address, house_number):
    house_number = re.sub(r'[\\]', '', house_number)
    cleaned_house_number = re.sub(r'[\\/]', '', house_number)
    if house_number in address or cleaned_house_number in address:
        return True
    else:
        return False
    
#Функция для заполнения БД координатами
def post_coordinates(uuid, latitude, longitude):
    url = 'http://192.168.111.61/UNF_FULL_WS/hs/setHomeCoordinates'
    
    headers = {
        'Authorization': data.BD_AUTHORIZATION,
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

uuid = "c3d567b6-9f3d-11e5-a904-3085a9f76558"
latitude = 53.311060
longitude = 59.143515

post_coordinates(uuid, latitude, longitude)

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

