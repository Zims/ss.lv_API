import requests
# Import required library
from xml.etree import cElementTree as ET
import time

class LinkCollector:
    real_estate_txts = []
    individual_property = []
    
    def __init__(self):
        self.links = []

    def check_sitemap(self):
        xmlstr = requests.get('https://www.ss.lv/sitemap.xml').text
        root = ET.fromstring(xmlstr)
        # extract all urls
        urls = []
        for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            urls.append(url.text)
        for url in urls:
            if "sitemap.msg.real-estate" in url:
                global real_estate_txts
                self.real_estate_txts.append(url)
        print("Real estate links:")
        print(self.real_estate_txts)

    def collector_property_links(self):
        for real_estate_txt in self.real_estate_txts:
            response = requests.get(real_estate_txt)

            # extract each line as a list element
            lines = response.text.splitlines()
            # filter out only the lines with links to flats in riga
            for line in lines:
                if "/lv/real-estate/flats/riga/" in line:
                    global individual_property
                    self.individual_property.append(line)
            time.sleep(2)
            print("Collecting links from each 'https://www.ss.lv/site_map/sitemap.msg.real-estate'. Sleeping for 2 seconds")
        # print(len(self.individual_property))

    # write to txt file
    def save_to_file(self):
        with open("ss_appartments.txt", "w") as f:
            for property in self.individual_property:
                f.write(property.strip() + "\n")
