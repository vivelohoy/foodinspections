Food Inspections
===============

An app for people to see what Chicago's food is like

Installation
============

    git clone https://github.com/vivelohoy/foodinspections.git
    cd /path/to/foodinspections
    pip install -r requirements.txt 
    python application.py
    
You should now see something like:

    * Running on http://127.0.0.1:5000/

If you visit localhost:5000(or whatever port your terminal displays) on your web browser, you should see the templates without any data on them. Navigating to links like the violations, from the navigation bar will cause errors. That's because we don't have any data yet.

To fix this problem first we stop our server.

    Note: To stop the server you can always press ctrl+c
    
Now run: 

    python createdb.py
    
The database has been created and you are ready to scrape:

    python scraper.py
    
After a couple of hours you should have the database with all the records. You can though not recommended hit ctrl+c during the scrape to finish the script prematurely and start looking at some data.

After finishing the scrape run python application.py again and have fun.

Reloading Data
==============

If you want to reload the data, you must first drop the records you downloaded previously as the scraper will pull in all new data from the beginning of time to the present day and the scraper gets tripped up if there are duplicate records.

If you're using the local SQLite database file you can simply delete the file and re-create it with:

    python createdb.py

If you've deployed this to an Amazon EC2 instance that's using an RDS instance for the database, you need to delete records in the relevant tables on that database server. First SSH to the EC2 instance where you should have environment variables set to the RDS connection details. Connect to the MySQL server with the command:

    mysql --user=$RDS_USERNAME --password=$RDS_PASSWORD --host=$RDS_HOSTNAME $RDS_DB_NAME

At the MySQL prompt, first delete all records from the `inspection_violations` table:

    DELETE FROM inspection_violations WHERE 1;

Follow this by deleting all records from the `violations` table:

    DELETE FROM violations WHERE 1;

Exit out of the MySQL shell. Now change directory to where you have this repository cloned on the server, activate your virtual environment, and re-run the scraper with:

    python scraper.py
