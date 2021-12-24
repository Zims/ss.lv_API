# from bs4 import BeautifulSoup
import requests
import lxml.html
from lxml import etree
import time

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

region_list = ["centre","agenskalns","yugla","imanta","ilguciems"]

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
                single_row.append(td.xpath('.//*/text()'))


        row_list.append(single_row)
        print(single_row)
    row_list = row_list[1:31]
    print(len(row_list[0]))

    for row in row_list:
        try:
            details = {
                "description": row[2][0].replace(',', '').replace('\n', '').replace('\t', '').replace('\r', ''),
                "address": row[3],
                "rooms": row[4],
                "area": row[5],
                "floor": row[6],
                "building_type": row[7],
                "rent/month": row[8].split()[0].replace(',', ''),
                "price": row[9].split()[0].replace(',', '')
            }
        except:
            details = {
                "description": row[2][0].replace(',', '').replace('\n', '').replace('\t', '').replace('\r', ''),
                "address": row[3][0],
                "rooms": row[4][0],
                "area": row[5][0],
                "floor": row[6][0],
                "building_type": row[7][0],
                "rent/month": row[8][0].replace(',', ''),
                "price": row[9][0].replace(',', ''),
            }
        
        appartment_list.append(details)
        print(details)


def write_csv(appartment_list, region):
    # write csv wit headers
    with open(f'{region}_appartment_list.csv', 'w') as csv_file:
        csv_file.write(
            'description,address,rooms,area(kvm.),floor,building_type,rent/month,price\n')
        for appartment in appartment_list:
            csv_file.write(
                f'{appartment["description"]},{appartment["address"]},{appartment["rooms"]},{appartment["area"]},{appartment["floor"]},{appartment["building_type"]},{appartment["rent/month"]},{appartment["price"]}\n')
        appartment_list.clear()


def main():
    for region in region_list:
        base_url = f"https://www.ss.lv/lv/real-estate/flats/riga/{region}/sell/"
        html_text = requests.get(base_url, headers=headers).text
        get_class(html_text)
        write_csv(appartment_list, region)
        time.sleep(1)



if __name__ == '__main__':
    main()
