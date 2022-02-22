import requests
from lxml import etree
import time
from datetime import datetime
import sqlite3
import random
from read_sitemap import LinkCollector

# Link collector has a method to read sitemap.xml 
# and return a list of links
link_collector = LinkCollector()
link_collector.check_sitemap()
link_collector.collector_property_links()
individual_property_links = link_collector.individual_property
print(f'{len(individual_property_links)} links collected from ss.lv')

new_individual_property_links = []
# define connection to database and create cursor
conn = sqlite3.connect('ss_all.sqlite3')
cur = conn.cursor()

# # read all links from database ss_all.sqlite3 all urls
# to check what is in the database already
cur.execute('''SELECT url FROM ss_all''')
all_urls = cur.fetchall()

# create a list of all urls in database
all_db_urls_list = []
for url in all_urls:
    all_db_urls_list.append(url[0])
print(f'{len(all_db_urls_list)} links collected from db')

# # compare all urls from database with all urls from sitemap using the set() function
# # and create a list of new urls only
new_individual_property_links = list(
    set(individual_property_links) - set(all_db_urls_list))
# new_individual_property_links = individual_property_links
print(f'{len(new_individual_property_links)} new links collected')

# print(f'{len(new_individual_property_links)} new links collected')

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

write_to_db = '''CREATE TABLE IF NOT EXISTS ss_all (id INTEGER PRIMARY KEY AUTOINCREMENT,
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
        cur.execute('''INSERT INTO ss_all
                    (description,city,rajons,street,rooms,size,floor,max_floor,series,item_type,extras,price,tx_type,date_added,url,added_to_db)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
                    (description, city, rajons, street, rooms, size, floor, max_floor, series, item_type, extras, price, tx_type, date_added, url, added_to_db,))
        conn.commit()

    db_query()

def remove_old_records():
    cur.execute('''DELETE FROM ss_all WHERE date_added < date('now','-11 month')''')
    # delete records where date_added is null
    cur.execute('''DELETE FROM ss_all WHERE date_added IS NULL''')
    print(f'{cur.rowcount} records deleted')
    conn.commit()

remove_old_records()

for url in new_individual_property_links:
    detail_parser(url.strip())
    # print url index
    print(individual_property_links.index(url))
    time.sleep(0.1)

remove_old_records()

todays_date = datetime.now().strftime('%Y-%m-%d')
# get all records date_added    from db from today
cur.execute('''SELECT date_added FROM ss_all WHERE date_added = ?''', (todays_date,))
all_urls = cur.fetchall()
print(f'{len(all_urls)} records for today')