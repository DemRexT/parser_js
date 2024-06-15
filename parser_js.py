import requests
import pandas as pd
from bs4 import BeautifulSoup
import datetime
import csv


current_date = datetime.datetime.now().strftime('%m-%d')

with open(f'magnit_{current_date}.csv', 'w', encoding='utf-8') as file:
    writer = csv.writer(file)

    writer.writerow(
        (
            'Продукт',
            'Новая цена',
            'Старая цена',
            'Процент скидки',
        )
    )

def all_tovar_str(offset):
    print(offset)
    url = f'https://magnit.ru/webgate/v1/promotions?categoryId&offset={offset}&limit=36&storeCode=992301&adult=true'
    headers = {
        'Accept': '*/*',
        'Accept-Language': 'ru,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Referer': 'https://magnit.ru/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
        'X-App-Version': '7.0.0',
        'X-Client-Name': 'magnit',
        'X-Device-ID': '963E75A0-DEBD-A7AC-3AC4-A0DF4FD7DF16',
        'X-Device-Platform': 'Web',
        'X-Device-Tag': 'disabled',
        'X-New-Magnit': 'true',
        'X-Platform-Version': 'Windows Chrome 122',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    responce = requests.get(url=url, headers=headers)

    return responce.json()

def products_str(response):

    products_raw = response.get('data', {})

    if len(products_raw) > 0:
        for product in products_raw:

            name = product.get("name", None)
            prise = float(product.get("price", None)) / 100 if product.get("price", None) != None else None
            oldPrice = float(product.get("oldPrice", None)) / 100 if product.get("oldPrice", None) != None else None
            sale = product.get("discountLabel", None)


            with open(f'magnit_{current_date}.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        name,
                        prise,
                        oldPrice,
                        sale,
                    )
                )





def main():


    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'Accept-Language': 'ru,en;q=0.9',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Referer': 'https://www.yandex.ru/',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-User': '?1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 YaBrowser/24.4.0.0 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "YaBrowser";v="24.4", "Yowser";v="2.5"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
    }

    of = requests.get(
        'https://magnit.ru/promo-catalog/?utm_source=magnit.ru&amp;utm_campaign=navbar&amp;utm_medium=promo&page=2',
        headers=headers
    )

    soup = BeautifulSoup(of.text, 'lxml')

    offsets = soup.find('nav', class_='pl-pagination__pager').find_all('li')[5].find('span', class_='pl-button__icon').text
    print(int(offsets)*36)
    for offset in range(0, (int(offsets)+1)*36, 36):
        response = all_tovar_str(offset)
        products_str(response)


if __name__ == '__main__':
    main()