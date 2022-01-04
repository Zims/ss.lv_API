import requests
from lxml import etree
import time

only_pardod = []
# open txt file with links to real estate
with open("ss_appartments.txt", "r") as f:
    # read line by line and add to list
    lines = f.readlines()
    # remove \n from each line
    lines = [line.strip() for line in lines]
# print(lines)
def filter_pardod(url):
    r = requests.get(url)
    # create a tree from the html string
    root = etree.HTML(r.text)
    # find by class name
    appartments = root.xpath('//h2[@class="headtitle"]/text()')
    print(appartments[2])
    
    try:
        if 'Pārdod' in appartments[2]:
            global only_pardod
            only_pardod.append(url)

            with open("ss_pardod.txt", "a") as f:
                f.write(url + "\n")
    except:
        pass

print("Filtering only pardod links:")
for line in lines[11587:]:
    # print line index
    print(lines.index(line))
    filter_pardod(line)
    time.sleep(0.1)

print(len(only_pardod))
print(only_pardod)
