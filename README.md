# ss.lv_API

1. Scrape a category of ss
2. Save data to SQLite
3. With FastAPI create data api for read purposes

Activate venv

It now has a db of flat adds for the last 2 days. (because of limited space on github you will need to create the initial db yourself)
Running scraper_classes checks for all flats in Riga listed on the site. 
Then compares the results to links already in the db. If a link is new it parses it and adds to db.
The scraper gets new links every minute and cross-references the db for existing duplicates. And only imports new ones. So the load on the site and db is minimal + there is a db query that runs once in a while and it drops any dupe records that made it in the db.

!!!Before running be sure to cd into "scrapers" folder!


The API 
Based on fastapi.
cd back to main.py location
run it using:
uvicorn main:app --reload
The API connects to the flats db. Endpoints are in the "/" path