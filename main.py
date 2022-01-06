from fastapi import FastAPI
import json
import sqlite3


app = FastAPI()

# Database connection
conn = sqlite3.connect('ss_db.sqlite3')
c = conn.cursor()

# queries
c.execute("SELECT * FROM ss_appartments ORDER BY id DESC")
appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]

c.execute("SELECT * FROM ss_appartments WHERE region = 'yugla' ORDER BY id DESC")
yugla_appartments = [dict(zip([key[0] for key in c.description], row)) for row in c.fetchall()]


# Endpoints #

@app.get("/")
def index():
    return f"Hello World! Go to /docs to see the docs."

@app.get("/all")
def centrs():
    return appartments

@app.get("/yugla")
def yugla():
    return yugla_appartments
