# from bs4 import BeautifulSoup
import requests
import lxml.html
from lxml import etree
import time
import json

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

region_list = ["centre", "agenskalns", "yugla", "imanta", "ilguciems"]

appartment_list = []


def get_class(html_text, region):
    tree = lxml.html.fromstring(html_text)
    tbody_table = tree.xpath('//table')[4]

    row_list = []
    for tr in tbody_table:
        single_row = []
        row_list.append(tr)
    for row in row_list[1:31]:
        try:
            description = row.find_class('d1')[0].find('a').text.replace(
                ',', "").replace('\n', "").replace('\t', "").replace('\r', "")
        except:
            description = "N/A"
        try:
            address = row[3].text
        except:
            address: row[3][0].text

        try:
            if row[4].text == "Citi":
                rooms = 0
            else:
                rooms = int(row[4].text)
        except:
            rooms = int(row[4][0].text)

        try:
            details = {
                "description": description,
                "address": address,
                "rooms": rooms,

                "area": int(row[5].text),
                "floor": int(row[6].text.split('/')[0]),
                "floor_max": int(row[6].text.split('/')[1]),
                "building_type": row[7].text,
                "rent/month": int(row[8].text.split()[0].replace(',', '')),
                "price": int(row[9].text.split()[0].replace(',', '')),
                "region": region,
                "url": f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
            }
        except:
            details = {
                "description": "N/A",
                "address": row[3][0].text,
                "rooms": int(row[4][0].text),
                "area": int(row[5][0].text),
                "floor": int(row[6][0].text.split('/')[0]),
                "floor_max": int(row[6][0].text.split('/')[1]),
                "building_type": row[7][0].text,
                "rent/month": int(row[8][0].text.replace(',', '')),
                "price": int(row[9][0].text.replace(',', '')),
                "region": region,
                "url": f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
            }

        appartment_list.append(details)


def write_csv(appartment_list, region):
    # write csv wit headers
    with open(f'results/{region}_appartment_list.csv', 'w') as csv_file:
        csv_file.write(
            'description,address,rooms,area(kvm.),floor,floor_max,building_type,rent/month,price,region,url\n')
        for appartment in appartment_list:
            csv_file.write(
                f'{appartment["description"]},{appartment["address"]},{appartment["rooms"]},{appartment["area"]},{appartment["floor"]},{appartment["floor_max"]},{appartment["building_type"]},{appartment["rent/month"]},{appartment["price"]},{region},{appartment["url"]}\n')
        appartment_list.clear()


def write_json(appartment_list, region):
    # write as utf-8 json
    with open(f'results/{region}_appartment_list.json', 'w') as json_file:
        json.dump(appartment_list, json_file, ensure_ascii=False)
        appartment_list.clear()


def main():
    for region in region_list:
        print(f'Scraping {region}')
        base_url = f"https://www.ss.lv/lv/real-estate/flats/riga/{region}/sell/"
        html_text = requests.get(base_url, headers=headers).text
        get_class(html_text, region)
        write_json(appartment_list, region)
        time.sleep(1)


if __name__ == '__main__':
    main()
