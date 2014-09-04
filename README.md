Food Inspections
===============

An app for people to see what Chicago's food is like

Installation
============

    mkdir -p /opt/python/run
    mkdir -p /opt/python/current
    cd /opt/python/run
    virtualenv venv
    source venv/bin/activate
    cd /opt/python/current
    git clone https://github.com/vivelohoy/foodinspections.git app
    cd app
    pip install -r requirements.txt

At this point, you have the basic Python library requirements set up. You'll now need to set the proper environment variables for your RDS instance running MySQL. Use the file `secretsrc.template` and fill in the missing details. Then copy this to your home directory like so:

    cp secretsrc.template ~/.secretsrc

Add the following line to the end of your `.bashrc` file to add these environment variables to your shell:

    source ~/.secretsrc

You can either log out/in or run `source ~/.bashrc` to apply these changes. When the environment variables are set (you can check this by running `env | grep RDS`), run the application server:

    python application.py
    
You should now see something like:

    * Running on http://127.0.0.1:5000/

If you visit [http://127.0.0.1:5000/](http://127.0.0.1:5000/) on your web browser, you should see the templates without any data on them. Navigating to links from the navigation bar will cause errors. That's because we don't have any data yet.

To fix this problem we must first stop our server. To stop the server you can always press CTRL-c.
    
Now run: 

    python createdb.py
    
The database has been created and you are ready to scrape:

    python scraper.py
    
After a couple of hours you should have the database with all the records. You can (though not recommended) hit CTRL-c during the scrape to finish the script prematurely and start looking at some data.

After finishing the scrape run `python application.py` again and have fun.

Scheduling Nightly Scrape
=========================

Included is a crontab configuration to download data on a nightly basis at midnight. The configuration is found in `crontab.backup`:

    #MAILTO="support@vivelohoy.com"
    0 0 * * * /opt/python/current/app/cron.sh

This assumes that you have this application installed in the path `/opt/python/current/app` and that you have a virtualenv created for the project, with requirements installed, located in `/opt/python/run/venv`.

Uncomment the first line of the `crontab.backup` file and change the email address there if you want the cron job output to be emailed somewhere automatically.

Import the crontab configuration with:

    crontab crontab.backup 