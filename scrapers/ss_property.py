from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
from datetime import datetime, timezone, timedelta
import pytz

tz=pytz.timezone("Europe/Riga")
time_now = datetime.now(tz)
format = "%Y-%m-%d-%T"
time_now = time_now.strftime(format)
ss_filename = f"output/{time_now}"

def refresh_time():
    tz=pytz.timezone("Europe/Riga")
    time_now = datetime.now(tz)
    format = "%Y-%m-%d-%T"
    time_now = time_now.strftime(format)
    global ss_filename
    ss_filename = f"output/{time_now}"

def scrape_ss(chosen_region):
    def parse_page(page=1):
        base_ss = 'https://www.ss.com'
        for row in rows:
            d = {}
            elements = row.find_all("td", {"class": "msga2-o pp6"})
            element_list = []
            for i in elements:
                element_list.append(i.text)
            try:
                d["address"] = element_list[0]
                try:
                    d["istabas"] = int(element_list[1])
                except:
                    d["istabas"] = "Nav norādīts"

                d["platiba"] = int(element_list[2])
                d["stavs"] = element_list[3]
                d["tips"] = element_list[4]
                d["cena_m2"] = int(element_list[5].replace(" €", "").replace(",", ""))
                d["cena(eiro)"] = int(element_list[-1].replace("  €", "").replace(",", ""))
                try:
                    temp_url = row.find("a", href=True)["href"]
                    d['links'] = f'{base_ss}{temp_url}'
                except:
                    d["links"] = None
                d["Vieta"] = chosen_region[0]
            except:
                d["address"] = None
                d["istabas"] = None
                d["platiba"] = None
                d["stavs"] = None
                d["tips"] = None
                d["cena_m2"] = None
                d["cena(eiro)"] = None
            d_list.append(d)
        refresh_time()

    headers = {'User-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}

    d_list = []
    print(chosen_region)
    if chosen_region[0] == "all":
        for page in range(1, 11):
            url = f"https://www.ss.com/lv/real-estate/flats/riga/{chosen_region[0]}/sell/page{page}.html"
            print(url)
            response = requests.get(url, headers=headers)
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            table = soup.select("table:nth-child(3)")
            rows = table[0].find_all("tr")
            time.sleep(2)
            parse_page(page)
    else:
        for page in range(1, 5):
            url = f"https://www.ss.com/lv/real-estate/flats/riga/{chosen_region[0]}/sell/page{page}.html"
            print(url)
            response = requests.get(url, headers=headers)
            content = response.text
            soup = BeautifulSoup(content, "html.parser")
            table = soup.select("table:nth-child(3)")
            rows = table[0].find_all("tr")
            time.sleep(2)
            parse_page(page)

    df = pd.DataFrame(d_list)
    # print(d_list)
    # vieta = df["Vieta"][5]

    # df.dropna().to_csv(f"{ss_filename}.csv")
    # df.dropna().to_excel(f"{ss_filename}_{chosen_region[0]}.xlsx")

        # import pandas as pd
    # Create a Pandas Excel writer using XlsxWriter as the engine.
    writer = pd.ExcelWriter(f"{ss_filename}_{chosen_region[0]}.xlsx", engine='xlsxwriter')

    # Convert the dataframe to an XlsxWriter Excel object. We also turn off the
    # index column at the left of the output dataframe.
    df.dropna().to_excel(writer, sheet_name='Sludinajumi')

    # Get the xlsxwriter workbook and worksheet objects.
    workbook  = writer.book
    worksheet = writer.sheets['Sludinajumi']

    # Get the dimensions of the dataframe.
    (max_row, max_col) = df.shape

    # Make the columns wider for clarity.
    worksheet.set_column(0,  max_col - 1, 12)

    # Set the autofilter.
    worksheet.autofilter(0, 0, max_row, max_col - 1)

    # Close the Pandas Excel writer and output the Excel file.
    writer.save()
    print("Done!")
