from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from datetime import datetime



app = FastAPI()

# Database connection
conn = sqlite3.connect('scrapers/ss_all.sqlite3', check_same_thread=False)
c = conn.cursor()

# queries
c.execute("SELECT * FROM ss_all_new ORDER BY id DESC")
# get 20 newest records
c.execute("SELECT * FROM ss_all_new ORDER BY id DESC LIMIT 50")

all_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]

templates = Jinja2Templates(directory="templates")

# Endpoints #

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')


@app.get("/today")
async def today(request: Request):
    todays_date = datetime.now().strftime("%Y-%m-%d")
    c.execute("SELECT * FROM ss_all_new WHERE date_added = ? ORDER BY added_to_db DESC", (todays_date,))
    # put them in a list
    todays_ads = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
    return todays_ads


@app.get("/places")
async def places(request: Request):
    # return all places in database
    # only unique values for rajons
    c.execute("SELECT DISTINCT district FROM ss_all_new")
    # put them in a list
    district = [row[0] for row in c.fetchall()]
    return district


@app.get("/{district}/{end_date}")
async def district(request: Request, district: str, end_date: str):
    district = district.replace('_', ' ')
    end_date = end_date.replace('_', '-')
    c.execute("SELECT * FROM ss_all_new WHERE district = ? AND date_added >= ? ORDER BY added_to_db DESC", (district, end_date))
    # put them in a list
    district_ads = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
    return district_ads


@app.get("/{place:str}")
def get_place(place):
    if place == "top100":
        # select only top 100 newest records
        c.execute("SELECT * FROM ss_all_new ORDER BY date_added DESC LIMIT 100")
        top100 = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
        return top100
    # elif place == "all":
    #         # select entire_db newest records
    #     c.execute("SELECT * FROM ss_all_new ORDER BY date_added DESC")
    #     entire_db_resp = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
    #     return entire_db_resp
    else:
        c.execute("SELECT * FROM ss_all_new WHERE district = ? ORDER BY added_to_db DESC LIMIT 300", (place,))
        place_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
        return place_appartments
