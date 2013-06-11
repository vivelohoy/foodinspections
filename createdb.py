import requests, json
from datetime import datetime
from inspections import *
from inspections.models.models import *

def create_db():
	db.create_all()

if __name__ == "__main__":
    create_db()
