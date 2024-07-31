from bs4 import BeautifulSoup
import requests

url = 'https://www.alta.ru/fias/socrname/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

table = soup.find('table', class_='bordered list-hover table-mobile js_sortable col-70 f-center m-col-xs-100')

short_names = []
for row in table.find_all('tr')[1:]:  # Пропуск заголовка
    columns = row.find_all('td')
    if len(columns) == 2:
        short_name = columns[1].text.strip().replace('.', '')  # Удаление точек
        short_names.append(short_name)

# Вывод списка
# for i in short_names:
#     print(i, end='|')

print(short_names)