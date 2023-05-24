from bs4 import BeautifulSoup  # Для парсинга HTML
from selenium import webdriver  # Для создания своего браузера
from selenium.webdriver.chrome.service import Service  # Для настройки Chrome
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36'}
options_chrome = webdriver.ChromeOptions()  # Настройки браузера
options_chrome.add_argument('headless')  # Настройки браузера (без визуального окна)
service = Service(executable_path="driver_chrome/chromedriver.exe")  # Настройки браузера
browser = webdriver.Chrome(service=service, options=options_chrome)  # Запуск браузера


class RatingFar:
    @staticmethod
    def get_rows():
        url = 'https://partreview.ru/top/fara-62/'
        browser.get(url)  # Открытие страницы с url
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')  # Создание обертки
        table_rating = soup.find("table", class_="tableRating")  # вся нужная таблица
        results = [[], [], [], [], []]
        position_row = table_rating.find("tbody").find_all("tr")
        for i in position_row:
            place = i.find("td").text.strip()
            logo = i.find_all("td")[1].find("span").get("data-original")
            manufacturer = i.find_all("td")[1].text.strip()
            rating = i.find_all("td")[2].text.strip()
            rating_pr = i.find_all("td")[3].text.strip()
            # print(place, manufacturer, rating, rating_pr)
            results[0].append(place)
            results[1].append(logo)
            results[2].append(manufacturer)
            results[3].append(rating)
            results[4].append(rating_pr)
        return results

    @staticmethod
    # часть для получения названий колонок
    def get_cols():
        url = 'https://partreview.ru/top/fara-62/'
        browser.get(url)  # Открытие страницы с url
        sleep(1)
        soup = BeautifulSoup(browser.page_source, 'lxml')  # Создание обертки
        table_rating = soup.find("table", class_="tableRating")  # вся нужная таблица
        result = []
        position_col = table_rating.find_all('span', class_="innerText")[:4]  # первая строка c колонками
        for i in position_col:
            title = i.text  # получили нужные названия колонок
            # print(title)
            result.append(title)
        return result


obj = RatingFar()  # экземпляр класса
# print(obj.get_rows())
# print(obj.get_cols())
