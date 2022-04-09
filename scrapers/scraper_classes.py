from itertools import count
import requests
from lxml import etree
import time
from datetime import datetime
import sqlite3
import random
import threading
from bs4 import BeautifulSoup

class AdScraper:
    def __init__(self, min_pages=10, mid_pages=20, max_pages=50):
        self.min_pages = min_pages
        self.mid_pages = mid_pages
        self.max_pages = max_pages
        self.url_collector = []
        self.user_agents = [
                                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                                'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
                            ]

    def get_urls_from_site(self, page_range=range(1,2)):
        for page_nr in page_range:
            response = requests.get(f'https://www.ss.lv/lv/real-estate/flats/riga/all/page{page_nr}.html')
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('form', id_='filter_frm')[0].select('table')[2].select('tr')
            for item in items:
                try:
                    extracted_url = f"https://www.ss.lv{item.select('a')[0].get('href')}"
                    self.url_collector.append(extracted_url)
                except:
                    continue
            print(f'Page {page_nr} collected')
            time.sleep(0.3)
        print(self.url_collector)
        return self.url_collector

    def scrape_single_page(self, url_collector):
        for collected_url in url_collector:
            try:
                r = requests.get(
                    collected_url, headers={'User-Agent': random.choice(self.user_agents)})
                root = etree.HTML(r.text)
            except:
                print("Nepareiza saite")
                print(collected_url)
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
                district = collected_url.split('/')[-2].replace('-', '_')
            except:
                district = None
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

            print(description)
            print(city)
            print(district)
            print(street)
            print(rooms)
            print(size)
            print(floor)
            print(max_floor)
            print(series)
            print(item_type)
            print(extras)
            print(price)
            print(date_added)
            print(tx_type)

    
class Database:
    def __init__(self):
        self.conn = sqlite3.connect('ss_all.sqlite3', check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(
            '''CREATE TABLE IF NOT EXISTS ss_all_new (id INTEGER PRIMARY KEY AUTOINCREMENT,
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
                                                                    )''')

    def remove_old_records(self):
        try:
            # remove old records from db older than 10 days
            self.cur.execute('''DELETE FROM ss_all_new WHERE date_added < date('now','-10 days')''')
            self.conn.commit()
            # remove broken records from db younger then a day
            self.cur.execute('''DELETE FROM ss_all_new WHERE date_added > date('now','+1 days')''')
            self.conn.commit()
            # set time every day at 3 am
            night_time = datetime.now().strftime('%H:%M')
            if night_time == '03:00':
                self.cur.execute('''DELETE FROM ss_all_new WHERE date_added < date('now','-1 days')''')
                self.conn.commit()            

        except:
            print('No records to delete')
            

            
db = Database()
# ads.get_urls_from_site()
db.remove_old_records()