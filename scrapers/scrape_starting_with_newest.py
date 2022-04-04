
from itertools import count
import requests
from lxml import etree
import time
from datetime import datetime
import sqlite3
import random
import threading
from bs4 import BeautifulSoup

url_collector = []
db_urls = []
counter = 999

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

conn = sqlite3.connect('ss_all.sqlite3', check_same_thread=False)
cur = conn.cursor()

def get_one_page(page_nr):
    response = requests.get(f'https://www.ss.lv/lv/real-estate/flats/riga/all/page{page_nr}.html')
    soup = BeautifulSoup(response.text, 'html.parser')
    items = soup.select('form', id_='filter_frm')[0].select('table')[2].select('tr')
    for item in items:
        try:
            extracted_url = f"https://www.ss.lv/{item.select('a')[0].get('href')}"
        except:
            continue
        global url_collector
        url_collector.append(extracted_url)

def fetch_all_db():
    try:
        # fetch all urls from db
        cur.execute('''SELECT url FROM ss_all_new''')
        rows = cur.fetchall()

        # create list of all urls in db
        for row in rows:
            global db_urls
            db_urls.append(row[0])
        return rows
    except:
        print('No records in db')

def create_db():
    try:
        write_to_db = '''CREATE TABLE IF NOT EXISTS ss_all_new (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                                    description TEXT,
                                                                    city TEXT,
                                                                    district TEXT,
                                                                    street TEXT,
                                                                    rooms INTEGER,
                                                                    size INTEGER,
                                                                    floor INTEGER,
                                                                    max_floor INTEGER,
                                                                    series TEXT,
                                                                    item_type TEXT,
                                                                    extras TEXT,
                                                                    price INTEGER,
                                                                    tx_type TEXT,
                                                                    date_added DATE,
                                                                    url TEXT,
                                                                    added_to_db TIMESTAMP
                                                                    )'''
        cur.execute(write_to_db)
    except:
        print('Error creating db')

def detail_parser(url):
    try:
        r = requests.get(
            url, headers={'User-Agent': random.choice(user_agents)})
        root = etree.HTML(r.text)
    except:
        print("Nepareiza saite")
        print(url)
    # create a tree from the html string
    try:
        tx_type = root.xpath('//h2[@class="headtitle"]/text()')
        tx_type = tx_type[-1].replace(' / ', '')
    except:
        tx_type = 'N/A'

    try:
        description = root.xpath('//div[@id="msg_div_msg"]/text()')
        description = " ".join(description).strip().replace('\t', '').replace('\n', '').replace('\r', '')
    except:
        description = "N/A"
    try:
        city = root.xpath('//td[@id="tdo_20"]/b/text()')[0]
    except:
        city = None
    try:
        district = root.xpath('//td[@id="tdo_856"]/b/text()')[0]
    except:
        district = None
    if district == "centrs":
        district = "centre"
    elif district == "Šampēteris-Pleskodāle":
        district = "sampeteris"
    elif district == "Pļavnieki":
        district = "plavnieki"
    elif district == "Mežciems":
        district = "mezciems"
    elif district == "Pļavnieki":
        district = "plavnieki"
    elif district == "Iļģuciems":
        district = "ilguciems"
    elif district == "Āgenskalns":
        district = "agenskalns"
    elif district == "Šķirotava":
        district = "skjirotava"
    elif district == "Ķīpsala":
        district = "kipsala"
    elif district == "Ķengarags":
        district = "kengarags"
    elif district == "Čiekurkalns":
        district = "ciekurkalns"
    elif district == "Zolitūde":
        district = "zolitude"
    elif district == "Ziepniekkalns":
        district = "ziepniekkalns"
    elif district == "Vecāķi":
        district = "vecaaki"
    elif district == "Vecrīga":
        district = "vecriga"
    elif district == "Vecmīlgrāvis":
        district = "vecmilgravis"
    elif district == "Torņakalns":
        district = "tornakalns"
    elif district == "Berģi":
        district = "bergi"
    elif district == "Dzegužkalns":
        district = "dzeguzkalns"
    elif district == "Bolderāja":
        district = "bolderaja"
    elif district == "Maskavas priekšpilsēta":
        district = "maskavas"
    elif district == "Krasta r-ns":
        district = "krasta"
    elif district == "Grīziņkalns":
        district = "grizinakalns"
    elif district == "Mežaparks":
        district = "mezaparks"
    elif district == "Mangaļi":
        district = "mangali"
    elif district == "Daugavgrīva":
        district = "daugavgriva"
    elif district == "Bieriņi":
        district = "bierini"
    elif district == "Jaunmīlgrāvis":
        district = "jaunmilgravis"
    elif district == "Beberbeķi":
        district = "beberbeki"
    elif district == "Kundziņsala":
        district = "kundzinsala"
    elif district == "Dreiliņi":
        district = "dreilini"
    elif district == "Mangaļsala":
        district = "mangalsala"
    else:
        try:
            district = district.lower()
        except:
            district = district

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
            '//td[@valign="bottom"]/table/*/*/text()')[0].replace('Datums: ', '').split(' ')[0].strip()

        # convert date_added from %dd.%mm.%yyyy to %yyyy-%mm-%dd
        date_added = date_added.split('.')[2]+'-'+date_added.split('.')[1]+'-'+date_added.split('.')[0]
        date_added = date_added.strip()

    except:
        date_added = None

    added_to_db = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # Write to db
    def db_query():
        # check if record exists in db then pass
            
        cur.execute('''INSERT INTO ss_all_new
                    (description,city,district,street,rooms,size,floor,max_floor,series,item_type,extras,price,tx_type,date_added,url,added_to_db)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (description, city, district, street, rooms, size, floor, max_floor, series, item_type, extras, price, tx_type, date_added, url, added_to_db,))
        conn.commit()

    db_query()

def running_update(page_count):
    try:
        for i in range(1,page_count):
            get_one_page(i)
            print('Page ' + str(i) + ' done')

        for url in url_collector:
            if url in db_urls:
                print("Already in db")
            else:
                print(url)
                t = threading.Thread(target=detail_parser, args=(url,),)
                t.start()
                time.sleep(0.07)
    except:
        print("Error")

def remove_old_records():
    try:
        # remove old records from db older than 300 days
        cur.execute('''DELETE FROM ss_all_new WHERE date_added < date('now','-300 days')''')
        conn.commit()
        # remove broken records from db younger then a day
        cur.execute('''DELETE FROM ss_all_new WHERE date_added > date('now','+1 days')''')
        conn.commit()
    except:
        print('No records to delete')

def delete_duplicate_records():
    try:
        cur.execute('''SELECT url,count(*) FROM ss_all_new GROUP BY url HAVING count(*) > 1''')
        duplicates = cur.fetchall()
        for duplicate in duplicates:
            cur.execute('''DELETE FROM ss_all_new WHERE url = ?''', (duplicate[0],))
            conn.commit()
            print(f'{duplicate[0]} deleted')
    except:
        print('No duplicates to delete')

def get_count_today():
    try:
        todays_date = datetime.now().strftime('%Y-%m-%d')
        cur.execute('''SELECT date_added FROM ss_all_new WHERE date_added = ?''', (todays_date,))
        all_urls = cur.fetchall()
        print(f'{len(all_urls)} records for today')
    except:
        print('No records for today')

while True:
    create_db()
    fetch_all_db()

    if counter % 1000 == 0:
        running_update(100)
        delete_duplicate_records()
    elif counter % 100 == 0:
        running_update(20)
        delete_duplicate_records()
    else:
        running_update(8)
        delete_duplicate_records()
    counter += 1
    get_count_today()
    print(f"Counter is at {counter}")
    db_urls = []
    remove_old_records()
    time.sleep(60)
