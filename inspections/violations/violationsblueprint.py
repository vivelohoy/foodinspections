from flask import Blueprint, render_template
from inspections.models.models import *
import datetime

violations_blueprint = Blueprint("violations_blueprint", __name__)

VIOLATIONS_PER_PAGE = 20

@violations_blueprint.route('/violations')
def show_violations():
    return(render_template('violations/violations.html', violations=Violations.query.order_by(Violations.violation_number)))


@violations_blueprint.route('/violations/<int:violation_number>')
def show_single_violation(violation_number):
    today = datetime.date.today()
    one_year = today - datetime.timedelta(days=365)
    violation = Violations.query.get_or_404(violation_number)
    inspections = Inspection.query.filter(Inspection.inspection_date > one_year).join(Inspection.violations, aliased=True).filter_by(violation_number=violation_number).all()
    return render_template('violations/single-violation.html' ,violation=violation, inspections=inspections)
