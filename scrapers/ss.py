# from bs4 import BeautifulSoup
import requests
import lxml.html
from lxml import etree
import time

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
    print(len(row_list))
    for row in row_list[1:31]:
        # print(
        #     f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}")
        print(row[3].text)

        try:
            details = {
                "description": row.find_class('d1')[0].find('a').text.replace(',', '').replace('\n', '').replace('\t', '').replace('\r', ''),
                "address": row[3].text,
                "rooms": row[4].text,
                "area": row[5].text,
                "floor": row[6].text,
                "building_type": row[7].text,
                "rent/month": row[8].text.split()[0].replace(',', ''),
                "price": row[9].text.split()[0].replace(',', ''),
                "region": region,
                "url": f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
            }
        except:
            details = {
                "description": "N/A",
                "address": row[3][0].text,
                "rooms": row[4][0].text,
                "area": row[5][0].text,
                "floor": row[6][0].text,
                "building_type": row[7][0].text,
                "rent/month": row[8][0].text.replace(',', ''),
                "price": row[9][0].text.replace(',', ''),
                "region": region,
                "url": f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
            }

        appartment_list.append(details)
        print(details)


def write_csv(appartment_list, region):
    # write csv wit headers
    with open(f'results/{region}_appartment_list.csv', 'w') as csv_file:
        csv_file.write(
            'description,address,rooms,area(kvm.),floor,building_type,rent/month,price,region,url\n')
        for appartment in appartment_list:
            csv_file.write(
                f'{appartment["description"]},{appartment["address"]},{appartment["rooms"]},{appartment["area"]},{appartment["floor"]},{appartment["building_type"]},{appartment["rent/month"]},{appartment["price"]},{region},{appartment["url"]}\n')
        appartment_list.clear()


def main():
    for region in region_list:
        base_url = f"https://www.ss.lv/lv/real-estate/flats/riga/{region}/sell/"
        html_text = requests.get(base_url, headers=headers).text
        get_class(html_text, region)
        write_csv(appartment_list, region)
        time.sleep(1)


if __name__ == '__main__':
    main()
