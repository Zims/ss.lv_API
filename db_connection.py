import sqlite3
import json
from results import *





c.execute('''INSERT INTO ss_appartments (description) VALUES (desc,)''')
conn.commit()
conn.close()



    for row in row_list[1:31]:
        try:
            description = row.find_class('d1')[0].find('a').text.replace(
                ',', "").replace('\n', "").replace('\t', "").replace('\r', "")
        except:
            description = "N/A"

        try:
            if row[3].text == None:
                address = "N/A"
            else:
                address = row[3].text.replace(',', "").replace('\n', "").replace('\t', "").replace('\r', "")
        except:
            address: row[3][0].text

        try:
            if row[4].text == "Citi":
                rooms = 0
            else:
                rooms = int(row[4].text)
        except:
            rooms = int(row[4][0].text)

        try:
            area = int(row[5].text)
        except:
            area = int(row[5][0].text)

        try:
            floor = int(row[6].text.split('/')[0])
        except:
            floor = int(row[6][0].text.split('/')[0])