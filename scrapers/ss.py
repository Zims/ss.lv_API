# from bs4 import BeautifulSoup
import requests
import lxml.html
from lxml import etree
import time

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

appartment_list = []


def get_class(html_text):
    tree = lxml.html.fromstring(html_text)
    tbody_table = tree.xpath('//table')[4]

    row_list = []
    for tr in tbody_table:
        single_row = []
        for td in tr:
            try:
                if len(td.text) > 0:
                    single_row.append(td.text)
            except:
                pass
        row_list.append(single_row)
        print(single_row)
    row_list = row_list[1:31]

    for row in row_list:
        try:
            details = {
                "address": row[0].replace(',', ' '),
                "rooms": row[1],
                "area": row[2],
                "floor": row[3],
                "building_type": row[4].replace(',', ' '),
                "rent/month": row[5].split(' ')[0].replace(',', ''),
                "price": row[6].split(' ')[0].replace(',', ''),
            }
        except:
            details = {
                "address": "",
                "rooms": "",
                "area": "",
                "floor": "",
                "building_type": "",
                "rent/month": "",
                "price": "",
            }
        appartment_list.append(details)


def write_csv(appartment_list):
    # write csv wit headers
    with open('ilguciems_appartment_list.csv', 'w') as csv_file:
        csv_file.write(
            'address,rooms,area,floor,building_type,rent/month,price\n')
        for appartment in appartment_list:
            csv_file.write(
                f'{appartment["address"]},{appartment["rooms"]},{appartment["area"]},{appartment["floor"]},{appartment["building_type"]},{appartment["rent/month"]},{appartment["price"]}\n')


def main():
    base_url = "https://www.ss.lv/lv/real-estate/flats/riga/ilguciems/sell/"
    html_text = requests.get(base_url, headers=headers).text
    get_class(html_text)
    write_csv(appartment_list)


if __name__ == '__main__':
    main()
