from flask import Blueprint, render_template, redirect, url_for, Response
from inspections.models.models import *
from sqlalchemy import func
import datetime

home_blueprint = Blueprint("home_blueprint", __name__)

@home_blueprint.route("/")
def show_home():
    today = datetime.date.today()
    seven_days_ago = today - datetime.timedelta(days=7)
    all_inspections = db.session.query(func.count(Inspection.inspection_id))
    total = all_inspections.all()

    inspections_this_week = all_inspections.filter(Inspection.inspection_date >= seven_days_ago)

    week_passed = inspections_this_week.filter_by(results = 'Pass').all()
    week_failed = inspections_this_week.filter_by(results = 'Fail').all()
    return render_template('home/home.html', total=total[0][0], total_this_week=inspections_this_week[0][0],passed=week_passed[0][0], failed=week_failed[0][0])
