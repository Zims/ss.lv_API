from fastapi import FastAPI, Request
import sqlite3
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Database connection
conn = sqlite3.connect('scrapers/ss_all.sqlite3', check_same_thread=False)
c = conn.cursor()

# queries
c.execute("SELECT * FROM ss_all ORDER BY id DESC")
# get 20 newest records
c.execute("SELECT * FROM ss_all ORDER BY id DESC LIMIT 50")

all_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]

templates = Jinja2Templates(directory="templates")

# Endpoints #

@app.get("/")
async def docs_redirect():
    return RedirectResponse(url='/docs')

# Opens index with a link to docs
# @app.get("/", response_class=HTMLResponse)
# async def index(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request})

@app.get("/places")
async def places(request: Request):
    # return all places in database
    # only unique values for rajons
    c.execute("SELECT DISTINCT rajons FROM ss_all")
    # put them in a list
    rajons = [row[0] for row in c.fetchall()]
    return rajons

@app.get("/{place:str}")
def get_place(place):
    if place == "all":
        # select only top 100 newest records
        c.execute("SELECT * FROM ss_all ORDER BY date_added DESC LIMIT 100")
        all_100 = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
        return all_100
    else:
        c.execute("SELECT * FROM ss_all WHERE rajons = ? ORDER BY date_added DESC", (place,))
        place_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
        return place_appartments
