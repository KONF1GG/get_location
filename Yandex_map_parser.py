from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

class YandexMapParser:
    def __init__(self):
        self.bad_coords = {'latitude': '53.302898', 'longitude': '59.140605'}
        o = Options()
        o.add_experimental_option("detach", True)
        o.add_argument(f'--user_agent={UserAgent().random}')
        # o.add_argument('--headless') # Uncomment this line for headless mode
        self.driver = webdriver.Chrome(options=o)
        self.driver.get('https://yandex.ru/maps')

    def get_location_from_Yandex(self, address):
        try:
            search_input = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, '//input[@placeholder="Поиск мест и адресов"]'))
            )

            search_input.send_keys(Keys.CONTROL + 'a')
            search_input.send_keys(Keys.BACKSPACE)

            search_input.send_keys(address)
            search_input.send_keys(Keys.RETURN)

            time.sleep(4)

            page = self.driver.page_source
            soup = BeautifulSoup(page, 'html.parser')

            coords_element = soup.find('div', class_='toponym-card-title-view__coords-badge')
            Yandex_address = soup.find('div', class_="card-title-view__wrapper").text

            if Yandex_address == None:
                return None

            if coords_element is not None:
                latitude, longitude = coords_element.text.split(', ')
                location_dict = {'latitude': latitude, 'longitude': longitude, 'Yandex_address': Yandex_address}
                if location_dict == self.bad_coords:
                    return None
            else:
                raise ValueError("Coordinates element not found.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            location_dict = None

        return location_dict

    def close_browser(self):
        self.driver.quit()