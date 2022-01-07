from fastapi import FastAPI
import json
import sqlite3


app = FastAPI()

# Database connection
conn = sqlite3.connect('ss_db.sqlite3', check_same_thread=False)
c = conn.cursor()

# queries
c.execute("SELECT * FROM ss_appartments ORDER BY id DESC")
all_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]


# Endpoints #

@app.get("/")
def index():
    return f"Hello World! Go to /docs to see the docs."

@app.get("/{place:str}")
def get_place(place):
    if place == "all":
        return all_appartments
    else:
        c.execute("SELECT * FROM ss_appartments WHERE region = ? ORDER BY id DESC", (place,))
        place_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]
        return place_appartments
