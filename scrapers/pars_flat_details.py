import requests
from lxml import etree
import time
import datetime
import sqlite3

with open("ss_appartments.txt", "r") as f:
    # read line by line and add to list
    lines = f.readlines()
    # remove \n from each line
    lines = [line.strip() for line in lines]

# define connection to database and create cursor
conn = sqlite3.connect('ss_db.sqlite3')
cur = conn.cursor()
# command1 = '''CREATE TABLE IF NOT EXISTS ss_appartments (id INTEGER PRIMARY KEY AUTOINCREMENT,
#                                                             description TEXT,
#                                                             address TEXT,
#                                                             rooms INTEGER,
#                                                             area INTEGER,
#                                                             floor INTEGER,
#                                                             floor_max INTEGER,
#                                                             building_type TEXT,
#                                                             rent_month INTEGER,
#                                                             price INTEGER,
#                                                             region TEXT,
#                                                             url TEXT
#                                                             )'''

write_to_db = '''CREATE TABLE IF NOT EXISTS ss_all_on_sale (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                            description TEXT,
                                                            city TEXT,
                                                            rajons TEXT,
                                                            street TEXT,
                                                            rooms INTEGER,
                                                            size INTEGER,
                                                            floor INTEGER,
                                                            max_floor INTEGER,
                                                            series TEXT,
                                                            item_type TEXT,
                                                            extras TEXT,
                                                            price INTEGER,
                                                            date_added TEXT
                                                            )'''                                                        
cur.execute(write_to_db)


# print(lines[606])
url = 'https://www.ss.lv/msg/lv/real-estate/flats/riga/ziepniekkalns/bcopi.html'


def detail_parser(root):
    try:
        description = root.xpath('//div[@id="msg_div_msg"]/text()')
        description = " ".join(description).strip().replace('\t', '')
    except:
        description = "N/A"
    try:
        city = root.xpath('//td[@id="tdo_20"]/b/text()')[0]
    except:
        city = None
    try:
        rajons = root.xpath('//td[@id="tdo_856"]/b/text()')[0]
    except:
        rajons = None
    try:
        street = root.xpath('//td[@id="tdo_11"]/b/text()')[0]
    except:
        street = None
    try:
        rooms = root.xpath('//td[@id="tdo_1"]/text()')[0]
    except:
        rooms = None
    try:
        size = root.xpath('//td[@id="tdo_3"]/text()')[0].split(' ')[0]
    except:
        size = None
    try:
        floor = root.xpath('//td[@id="tdo_4"]/text()')[0].split('/')[0]
    except:
        floor = None
    try:
        max_floor = root.xpath('//td[@id="tdo_4"]/text()')[0].split('/')[1]
    except:
        max_floor = None
    try:
        series = root.xpath('//td[@id="tdo_6"]/text()')[0]
    except:
        series = None
    try:
        item_type = root.xpath('//td[@id="tdo_2"]/text()')[0]
    except:
        item_type = None
    try:
        extras = root.xpath('//td[@id="tdo_1734"]/text()')[0].split(', ')
    except:
        extras = None
    try:
        price = root.xpath(
            '//td[@id="tdo_8"]/text()')[0].split('€')[0].replace(' ', '')
    except:
        price = None
    try:
        date_added = root.xpath(
            '//td[@valign="bottom"]/table/*/*/text()')[0].replace('Datums: ', '')
    except:
        date_added = None

        # Write to db
    cur.execute('''INSERT INTO ss_all_on_sale 
                (description,city,rajons,street,rooms,size,floor,max_floor,series,item_type,extras,price,date_added) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (description, city, rajons, street,rooms,size,floor,max_floor,series,item_type,extras,price,date_added,))
    conn.commit()


def pardod_check(url):
    # look for only pardod links
    r = requests.get(url)
    # create a tree from the html string
    root = etree.HTML(r.text)
    # find by class name
    appartments = root.xpath('//h2[@class="headtitle"]/text()')
    try:
        if 'Pārdod' in appartments[2]:
            print("Pārdod atrasts. Turpinu darbu.")
            detail_parser(root)
            return True
            # parse
    except:
        pass

for url in lines[0:1000]:
    pardod_check(url)
    time.sleep(1)

# # print(pardod_check(url))
# r = requests.get(url)
# # create a tree from the html string
# root = etree.HTML(r.text)
# detail_parser(root)
