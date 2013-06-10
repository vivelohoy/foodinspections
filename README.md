Food Inspections
===============

An app for people to see what Chicago's food is like

Installation
============

    git clone https://github.com/vivelohoy/foodinspections.git
    cd /path/to/foodinspections
    pip install -r requirements.txt 
    python run.py
    
You should now see something like:

    * Running on http://127.0.0.1:5000/

If you visit localhost:5000(or whatever port your terminal displays) on your web browser, you should see the templates without any data on them. Navigating to links like the violations, from the navigation bar will cause errors. That's because we don't have any data yet.

To fix this problem first we stop our server.

    Note: To stop the server you can always press ctrl+c
    
Now run python in interactive mode:

    python
    >>> from scraper import create_db
    >>> create_db()
    
The database has been created and you are ready to scrape:

    python scraper.py
    
After a couple of hours you should have the database with all the records. You can though not recommended hit ctrl+c during the scrape to finish the script prematurely and start looking at some data.

After finishing the scrape run python run.py again and have fun.
