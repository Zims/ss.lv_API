# ss.lv_API

1. Scrape a category of ss
2. Save data to SQLite
3. With FastAPI create data api for read purposes


It now has a db of 17k+ flats
Running parse_flat_detail.py checks for all flats listed on the site. 
Then compares the results to links already in the db. If a link is new it parses it and adds to db.

!!!Before running be sure to cd into "scrapers" folder!

First run will take a lot of time as it parses 17k flats. After that it only adds new listings.