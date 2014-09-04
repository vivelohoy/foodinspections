#! /bin/bash
# Set some environment variables we need for the scraper
source /home/ec2-user/.secretsrc

cd /opt/python
source run/venv/bin/activate

python current/app/scraper.py