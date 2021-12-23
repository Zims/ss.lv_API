from bs4 import BeautifulSoup
import requests
import time

base_url = "https://www.ss.lv/lv/real-estate/flats/riga/"

response = requests.get(base_url)
