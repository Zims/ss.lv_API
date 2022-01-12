import requests
# Import required library
from xml.etree import cElementTree as ET
import time

real_estate_txts = []
individual_property = []


def check_sitemap():
    xmlstr = requests.get('https://www.ss.lv/sitemap.xml').text
    root = ET.fromstring(xmlstr)

    # extract all urls
    urls = []
    for url in root.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.append(url.text)
    for url in urls:
        if "sitemap.msg.real-estate" in url:
            global real_estate_txts
            real_estate_txts.append(url)
    print("Real estate links:")
    print(real_estate_txts)

def collector_property_links():
    for real_estate_txt in real_estate_txts:
        response = requests.get(real_estate_txt)

        # extract each line as a list element
        lines = response.text.splitlines()
        for line in lines:
            if "/lv/real-estate/flats/riga/" in line:
                global individual_property
                individual_property.append(line)
        time.sleep(5)
        print("Individual property links:")
        for property in individual_property:
            print(property)
        print("Sleeping for 5 seconds")
    print(len(individual_property))

def save_to_file():
    with open("scrapers/ss_appartments.txt", "w") as f:
        for property in individual_property:
            f.write(property.strip() + "\n")


check_sitemap()
collector_property_links()
save_to_file()
