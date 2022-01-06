# from bs4 import BeautifulSoup
import requests
import lxml.html
from lxml import etree
import time
import sqlite3

# define connection to database and create cursor
conn = sqlite3.connect('ss_db.sqlite3')
c = conn.cursor()
command1 = '''CREATE TABLE IF NOT EXISTS ss_appartments (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            description TEXT, 
                                                            address TEXT,
                                                            rooms INTEGER,
                                                            area INTEGER,
                                                            floor INTEGER,
                                                            floor_max INTEGER,
                                                            building_type TEXT,
                                                            rent_month INTEGER,
                                                            price INTEGER,
                                                            region TEXT,
                                                            url TEXT
                                                            )'''
c.execute(command1)

headers = {
    'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

region_list = ["centre", "agenskalns", "yugla", "imanta", "ilguciems", "kengarags", "teika", "ziepniekkalns"]

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

        if type(row[3].text) == str:
            address = row[3].text
        elif type(row[3][0].text) == str:
            address = row[3][0].text
        else:
            address = "N/A"

        try:
            if row[4].text == "Citi":
                rooms = 0
            else:
                rooms = int(row[4].text)
        except:
            rooms = int(row[4][0].text)

        try:
            area = int(row[5].text)
        except:
            area = int(row[5][0].text)

        try:
            floor = int(row[6].text.split('/')[0])
        except:
            floor = int(row[6][0].text.split('/')[0])
        
        try:
            floor_max = int(row[6].text.split('/')[1])
        except:
            floor_max = int(row[6][0].text.split('/')[1])

        try:
            building_type = row[7].text
        except:
            building_type = row[7][0].text

        try:
            rent_month = int(row[8].text.split()[0].replace(',', ''))
        except:
            rent_month = int(row[8][0].text.replace(',', ''))
        
        try:
            price = int(row[9].text.split()[0].replace(',', ''))
        except:
            price = int(row[9][0].text.replace(',', ''))

        try:
            region = region
        except:
            region = "N/A"
        
        try:
            url = f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
        except:
            url = f"https://www.ss.lv{row.find_class('msga2')[1].find('a').get('href')}"
        
        # Write to db
        c.execute('''INSERT INTO ss_appartments 
                    (description,address,rooms,area,floor,floor_max,building_type,rent_month,price,region,url) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                  (description, address, rooms, area, floor,floor_max,building_type,rent_month,price,region,url,))
        conn.commit()


def main():
    for region in region_list:
        print(f'Scraping {region}')
        base_url = f"https://www.ss.lv/lv/real-estate/flats/riga/{region}/sell/"
        html_text = requests.get(base_url, headers=headers).text
        get_class(html_text, region)
        time.sleep(1)


if __name__ == '__main__':
    main()
    conn.close()
