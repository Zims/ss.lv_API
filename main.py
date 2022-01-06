from fastapi import FastAPI
import json
import sqlite3


app = FastAPI()

conn = sqlite3.connect('ss_db.sqlite3')
c = conn.cursor()

# queries
c.execute("SELECT * FROM ss_appartments")
whole_db = c.fetchall()
c.execute("SELECT * FROM ss_appartments WHERE region='yugla'")
yugla_db = c.fetchall()


@app.get("/")
def index():
    return f"Hello World! Go to /docs to see the docs."

@app.get("/all")
def centrs():
    return whole_db

@app.get("/yugla")
def yugla():
    return yugla_db