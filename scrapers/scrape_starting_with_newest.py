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

conn = sqlite3.connect('ss_all.sqlite3', check_same_thread=False)
cur = conn.cursor()

def fetch_all_db():
    # fetch all descriptions from db
    cur.execute('''SELECT url FROM ss_all_new''')
    rows = cur.fetchall()
    cur.execute('''DELETE FROM ss_all WHERE date_added < date('now','-12 month')''')
    print(f'{cur.rowcount} records deleted')
    conn.commit()


    for row in rows:
        global db_urls
        db_urls.append(row[0])
    return rows

try:
    fetch_all_db()
except:
    print('No db found')
existing_urls = db_urls


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

write_to_db = '''CREATE TABLE IF NOT EXISTS ss_all_new (id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                                                            tx_type TEXT,
                                                            date_added DATE,
                                                            url TEXT,
                                                            added_to_db TIMESTAMP
                                                            )'''
cur.execute(write_to_db)

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
        rajons = root.xpath('//td[@id="tdo_856"]/b/text()')[0]
    except:
        rajons = None
    if rajons == "centrs":
        rajons = "centre"
    elif rajons == "Šampēteris-Pleskodāle":
        rajons = "sampeteris"
    elif rajons == "Pļavnieki":
        rajons = "plavnieki"
    elif rajons == "Mežciems":
        rajons = "mezciems"
    elif rajons == "Pļavnieki":
        rajons = "plavnieki"
    elif rajons == "Iļģuciems":
        rajons = "ilguciems"
    elif rajons == "Āgenskalns":
        rajons = "agenskalns"
    elif rajons == "Šķirotava":
        rajons = "skjirotava"
    elif rajons == "Ķīpsala":
        rajons = "kipsala"
    elif rajons == "Ķengarags":
        rajons = "kengarags"
    elif rajons == "Čiekurkalns":
        rajons = "ciekurkalns"
    elif rajons == "Zolitūde":
        rajons = "zolitude"
    elif rajons == "Ziepniekkalns":
        rajons = "ziepniekkalns"
    elif rajons == "Vecāķi":
        rajons = "vecaaki"
    elif rajons == "Vecrīga":
        rajons = "vecriga"
    elif rajons == "Vecmīlgrāvis":
        rajons = "vecmilgravis"
    elif rajons == "Torņakalns":
        rajons = "tornakalns"
    elif rajons == "Berģi":
        rajons = "bergi"
    elif rajons == "Dzegužkalns":
        rajons = "dzeguzkalns"
    elif rajons == "Bolderāja":
        rajons = "bolderaja"
    elif rajons == "Maskavas priekšpilsēta":
        rajons = "maskavas"
    elif rajons == "Krasta r-ns":
        rajons = "krasta"
    elif rajons == "Grīziņkalns":
        rajons = "grizinakalns"
    elif rajons == "Mežaparks":
        rajons = "mezaparks"
    elif rajons == "Mangaļi":
        rajons = "mangali"
    elif rajons == "Daugavgrīva":
        rajons = "daugavgriva"
    elif rajons == "Bieriņi":
        rajons = "bierini"
    elif rajons == "Jaunmīlgrāvis":
        rajons = "jaunmilgravis"
    elif rajons == "Beberbeķi":
        rajons = "beberbeki"
    elif rajons == "Kundziņsala":
        rajons = "kundzinsala"
    elif rajons == "Dreiliņi":
        rajons = "dreilini"
    elif rajons == "Mangaļsala":
        rajons = "mangalsala"
    else:
        try:
            rajons = rajons.lower()
        except:
            rajons = rajons

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
                    (description,city,rajons,street,rooms,size,floor,max_floor,series,item_type,extras,price,tx_type,date_added,url,added_to_db)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (description, city, rajons, street, rooms, size, floor, max_floor, series, item_type, extras, price, tx_type, date_added, url, added_to_db,))
        conn.commit()

    db_query()


for i in range(1,15):
    get_one_page(i)
    print('Page ' + str(i) + ' done')

for url in url_collector:
    if url in existing_urls:
        print("Already in db")
    else:
        print(url)
        t = threading.Thread(target=detail_parser, args=(url,),)
        t.start()
        time.sleep(0.07)
