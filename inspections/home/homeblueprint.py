from flask import Blueprint, render_template, redirect, url_for, Response
from inspections.models.models import *
from sqlalchemy import func
import datetime

home_blueprint = Blueprint("home_blueprint", __name__)

@home_blueprint.route("/")
def show_home():
    today = datetime.date.today()
    
    thirty_days_ago = today - datetime.timedelta(days=30)

    inspections_this_month = Inspection.query.filter(Inspection.inspection_date >= thirty_days_ago)

    month_passed = inspections_this_month.filter_by(results = 'Pass').all()
    month_failed = inspections_this_month.filter_by(results = 'Fail').all()

    return render_template('home/home.html',passed=len(month_passed), failed=len(month_failed))
