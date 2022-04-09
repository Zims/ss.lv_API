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

    def get_one_page(self, page_range=range(1,50)):
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






# ads = AdScraper()
# ads.get_one_page()