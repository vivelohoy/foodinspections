# Food Inspections

An app for people to see what Chicago's food is like.

## Develop

After cloning this repository, create a virtual environment and install the requirements:

    virtualenv venv && source venv/bin/activate
    pip install -r requirements.txt

You'll need to create a local copy of the database. Do this with:

    python createdb.py

After the `inspections.db` SQLite database file is created, you must populate it with real data. Run the scraper with:

    python scraper.py

Run the application server with:

    python application.py
    
Open the application in your browser using the address http://127.0.0.1:5000/

## Deploy

This application is designed to run on [AWS](https://aws.amazon.com/) using the [Elastic Beanstalk](https://aws.amazon.com/elasticbeanstalk/) service. In order to deploy, you need to have the [awsebcli](http://docs.aws.amazon.com/elasticbeanstalk/latest/dg/eb-cli3-getting-set-up.html) client installed on your system and have the AWS access key ID and secret access key.

In the `foodinspections` folder, run (this only needs to be done once per machine):

    eb init

When you're ready to deploy the new code, run:

    eb deploy

## TODO

* How to set up from scratch
* How to use RDS
* How to schedule scraper.py to run nightly
