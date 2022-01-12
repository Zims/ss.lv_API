import requests
from lxml import etree
import time
import datetime
import sqlite3
import random

user_agents = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
]

with open("ss_appartments.txt", "r") as f:
    # read line by line and add to list
    lines = f.readlines()
    # remove \n from each line
    lines = [line.strip() for line in lines]

# define connection to database and create cursor
conn = sqlite3.connect('ss_db.sqlite3')
cur = conn.cursor()

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
                                                            date_added TEXT,
                                                            url TEXT
                                                            )'''                                                        
cur.execute(write_to_db)

def detail_parser(root,url):
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
        extras = root.xpath('//td[@id="tdo_1734"]/text()')[0]
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
                (description,city,rajons,street,rooms,size,floor,max_floor,series,item_type,extras,price,date_added,url) 
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                (description, city, rajons, street,rooms,size,floor,max_floor,series,item_type,extras,price,date_added,url,))
    conn.commit()

def pardod_check(url):
    # look for only pardod links
    r = requests.get(url, headers={'User-Agent': random.choice(user_agents)})
    # create a tree from the html string
    root = etree.HTML(r.text)
    # find by class name
    appartments = root.xpath('//h2[@class="headtitle"]/text()')
    try:
        if 'Pārdod' in appartments[2]:
            print("Pārdod atrasts!!!")
            detail_parser(root,url)
            return True
        else:
            print("Pārdod nav atrasts...")
            return False
    except:
        pass

for url in lines[100:200]:
    # print url index
    if lines.index(url) % 25 == 0:
        print(lines.index(url))
    pardod_check(url)
    time.sleep(0.3)
