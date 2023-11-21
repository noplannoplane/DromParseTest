import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import urllib.request
import shutil
import zipfile

# URL страницы с объявлениями
start_url = "https://auto.drom.ru/all/page1/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"

# заголовки для запросов
headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

# получаем ссылки на все страницы с объявлениями
start_response = requests.get(start_url)
start_soup = BeautifulSoup(start_response.text, 'html.parser')
pages = [start_url]
for pages_urls in start_soup.find_all('a', class_='css-14wh0pm e1lm3vns0'):
    pages.append(pages_urls['href'])

for i in range(2, 5):
    url = f"https://auto.drom.ru/all/page{i}/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"
    pages.append(url)
    
# функция для получения данных об автомобиле
def get_car_data(car_url):
    car_req = requests.get(car_url, headers=headers)
    car_src = car_req.text
    car_soup = BeautifulSoup(car_src, 'html.parser')
    car_info = car_soup.find_all('div', class_='css-1j5vzv4 e1w8x3rg2')
    car_data = {}
    for info in car_info:
        if 'Марка' in info.text:
            car_data['Марка'] = info.find('a').text.strip()
            car_data['Модель'] = info.find_all('a')[1].text.strip()
            car_data['Поколение'] = info.find_all('a')[2].text.strip()
        elif 'Комплектация' in info.text:
            car_data['Комплектация'] = info.find('a').text.strip()
        elif 'Пробег' in info.text:
            car_data['Пробег'] = info.find('span').text.strip()
            if 'без пробега по РФ' in info.text:
                car_data['Пробег по РФ'] = 'нет'
            else:
                car_data['Пробег по РФ'] = 'есть'
        elif 'Цвет' in info.text:
            car_data['Цвет'] = info.find('span').text.strip()
        elif 'Тип кузова' in info.text:
            car_data['Тип кузова'] = info.find('span').text.strip()
        elif 'Мощность двигателя' in info.text:
            car_data['Мощность двигателя'] = info.find('span').text.strip()
        elif 'Тип топлива' in info.text:
            car_data['Тип топлива'] = info.find('span').text.strip()
        elif 'Объем двигателя' in info.text:
            car_data['Объем двигателя'] = info.find('span').text.strip()
    return car_data

# # функция для сохранения фотографий
# def save_photos(car_url, car_num):
#     car_req = requests.get(car_url, headers=headers)
#     car_src = car_req.text
#     car_soup = BeautifulSoup(car_src, 'html.parser')
#     photos = car_soup.find_all('img', class_='css-1v1pro2 e1s0w0kz0')
#     if not photos:
#         return
#     os.mkdir(f'Result_Crown/{car_num}')
#     for i, photo in enumerate(photos):
#         photo_url = photo.get('src')
#         filename = f'Result_Crown/{car_num}/{i}.jpg'
#         urllib.request.urlretrieve(photo_url, filename)

# # список для хранения данных об автомобилях
# car_data_list = []

# # получаем данные об автомобилях на каждой странице
# def car_url_data(car_url, car_data_list):
#     for i, page in enumerate(pages):
#         req = requests.get(page, headers=headers)
#         src = req.text
#         soup = BeautifulSoup(src, "lxml")
#         all_ads_hrefs = soup.find_all(class_=("css-xb5nz8 e1huvdhj1"))
#         if not all_ads_hrefs:
#             continue
#         for class_ in all_ads_hrefs:
#             for span in class_.find_all('span'):
#                 span.append(' ')
#             for div in class_.find_all('div'):
#                 div.append(' ')

#         for item in all_ads_hrefs:
#             item_text = item.text.replace(' ', '')
#             item_href = "h" + item.get("href")[1:]
#             # проверяем, что объявление соответствует требованиям
#             if 'Toyota Crown' in item_text and ('15' in item_text or '16' in item_text) and 'Владивосток' in item_text and 'Уссурийск' in item_text and 'Под заказ' not in item_text and 'В пути' not in item_text and 'Требует ремонта' not in item_text:
#                 car_num = item_href.split('/')[-2]
#                 car_data = {'Номер на Дроме': car_num, 'URL объявления': item_href}
#                 car_data.update(get_car_data(item_href))
#                 price_info = item.find('div', class_='css-1fj5j8v e1w8x3rg0')
#                 if price_info:
#                     car_data['Цена продажи'] = price_info.find('span').text.strip()
#                     car_data['Отметка цены'] = price_info.find('div', class_='css-1h1j0y3 e1w8x3rg1').text.strip()
#                 else:
#                     car_data['Цена продажи'] = 'null'
#                     car_data['Отметка цены'] = 'null'
#                 # сохраняем фотографии
#                 save_photos(item_href, car_num)
#                 car_data_list.append(car_data)

# def main():
#     url = "https://auto.drom.ru/all/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.text, 'html.parser')

#     ads = soup.select('.css-ylksg2 a.css-105aqej')

#     os.makedirs('Result_Crown', exist_ok=True)
#     os.chdir('Result_Crown')

#     for ad in ads:
#         parse_advert(ad['href'])

#     # Создаем архив
#     with zipfile.ZipFile('Result_Crown.zip', 'w') as zipf:
#         zipf.write('Data.csv')

# def main():
#     all_ads_hrefs = soup.find_all(class_=("css-xb5nz8 e1huvdhj1"))
#     car_data_list = []
#     for item in all_ads_hrefs:
#         item_text = item.text.replace(' ', '')
#         item_href = "h" + item.get("href")[1:]
#         # проверяем, что объявление соответствует требованиям
#         if 'Toyota Crown' in item_text and ('15' in item_text or '16' in item_text) and 'Владивосток' in item_text and 'Уссурийск' in item_text and 'Под заказ' not in item_text and 'В пути' not in item_text and 'Требует ремонта' not in item_text:
#             car_num = item_href.split('/')[-2]
#             car_data = {'Номер на Дроме': car_num, 'URL объявления': item_href}
#             car_data.update(get_car_data(item_href))
#             price_info = item.find('div', class_='css-1fj5j8v e1w8x3rg0')
#             if price_info:
#                 car_data['Цена продажи'] = price_info.find('span').text.strip()
#                 car_data['Отметка цены'] = price_info.find('div', class_='css-1h1j0y3 e1w8x3rg1').text.strip()
#             else:
#                 car_data['Цена продажи'] = 'null'
#                 car_data['Отметка цены'] = 'null'
#             # сохраняем фотографии
#             save_photos(item_href, car_num)
#             car_data_list.append(car_data)
#     print(car_data_list)
#     car_data = {}
#     car_data['Номер объявления'] = class_.find('a')['href'].split('/')[-2]
#     car_data['Цена'] = class_.find('span', class_='css-1q5x9h6 e1wijj2y4').text.strip().replace('\xa0', ' ')
#     car_data['Год выпуска'] = class_.find_all('span')[1].text.strip()
#     car_data['Пробег'] = class_.find_all('span')[2].text.strip()
#     car_data['Тип кузова'] = class_.find_all('span')[3].text.strip()
#     car_data['Тип топлива'] = class_.find_all('span')[4].text.strip()
#     car_data['Объем двигателя'] = class_.find_all('span')[5].text.strip()
#     car_data['Мощность двигателя'] = class_.find_all('span')[6].text.strip()
#     car_data['Привод'] = class_.find_all('span')[7].text.strip()
#     car_data['КПП'] = class_.find_all('span')[8].text.strip()
#     car_data.update(get_car_data(class_.find('a')['href']))
#     car_data_list.append(car_data)
#     save_photos(class_.find('a')['href'], car_data['Номер объявления'])
#     print(f'Страница {i+1} обработана')
#     return car_data_list
# if __name__ == '__main__':
#     main()

# # сохраняем данные в файл csv
# def save_csv(car_data_list):
#     with open('Result_Crown/cars.csv', 'w', encoding='utf-8', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(car_data_list[0].keys())
#         for car_data in car_data_list:
#             writer.writerow(car_data.values())

# # сохраняем данные в файл json
# def save_json(car_data_list):
#     with open('Result_Crown/cars.json', 'w', encoding='utf-8') as file:
#         json.dump(car_data_list, file, ensure_ascii=False, indent=4)

# # архивируем папку с фотографиями
# def zip_photos():
#     shutil.make_archive('Result_Crown', 'zip', 'Result_Crown')

# car_data_list = car_url_data(start_url, car_data_list)
# save_csv(car_data_list)
# save_json(car_data_list)
# zip_photos()
# # записываем данные об автомобилях в CSV-файл
# with open("Result_Crown/Data.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(['Номер на Дроме', 'URL объявления', 'Марка', 'Модель', 'Цена продажи', 'Отметка цены', 'Поколение', 'Комплектация', 'Пробег', 'Пробег по РФ', 'Цвет', 'Тип кузова', 'Мощность двигателя', 'Тип топлива', 'Объем двигателя'])
#     for car_data in car_data_list:
#         writer.writerow([car_data.get(key, 'null') for key in ['Номер на Дроме', 'URL объявления', 'Марка', 'Модель', 'Цена продажи', 'Отметка цены', 'Поколение', 'Комплектация', 'Пробег', 'Пробег по РФ', 'Цвет', 'Тип кузова', 'Мощность двигателя', 'Тип топлива', 'Объем двигателя']])

# # создаем архив с результатами
# shutil.make_archive('Result_Crown', 'zip', 'Result_Crown')

# # удаляем папку с результатами
# shutil.rmtree('Result_Crown')
            



# start_req = requests.get(start_url, headers=headers)
# start_src = start_req.text
# start_response = requests.get(start_url)
# start_soup = BeautifulSoup(start_response.text, 'html.parser')
# pages = [start_url]
# for pages_urls in start_soup.find_all('a', class_='css-14wh0pm e1lm3vns0'):
#     pages.append(pages_urls['href'])

# for i in range(2, 5):
#     url = f"https://auto.drom.ru/all/page{i}/?cid[]=23&cid[]=170&order=price&multiselect[]=9_4_15_all&multiselect[]=9_4_16_all&pts=2&damaged=2&unsold=1"
#     pages.append(url)

# all_ads_dict = {}
# for i, page in enumerate(pages):
#     req = requests.get(page, headers=headers)
#     src = req.text
#     soup = BeautifulSoup(src, "lxml")
#     all_ads_hrefs = soup.find_all(class_=("css-xb5nz8 e1huvdhj1"))
#     if not all_ads_hrefs:
#         continue
#     for class_ in all_ads_hrefs:
#         for span in class_.find_all('span'):
#             span.append(' ')
#         for div in class_.find_all('div'):
#             div.append(' ')

#     for item in all_ads_hrefs:
#         item_text = item.text.replace(' ', '')
#         item_href = "h" + item.get("href")[1:]
#         all_ads_dict[item_text] = item_href

# # записываем данные заголовков в json файл
# with open('all_ads_headers.json', 'w', encoding='utf-8') as f:
#     json.dump(all_ads_dict, f, ensure_ascii=False, indent=4)


# # запись данных заголовков в CSV-файл
# with open("all_ads_headers.csv", "w", newline="", encoding="utf-8") as file:
#     writer = csv.writer(file)
#     writer.writerow(["Название", "Год",  "Ссылка", ....])
#     for item_text, item_href in all_ads_dict.items():
#         writer.writerow([item_text, item_href])