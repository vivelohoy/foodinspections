from flask import Blueprint, render_template
from inspections.models.models import *

violations_blueprint = Blueprint("violations_blueprint", __name__)

VIOLATIONS_PER_PAGE = 20

@violations_blueprint.route('/violations')
def show_violations():
    return(render_template('violations/violations.html', violations=Violations.query.order_by(Violations.violation_number)))


@violations_blueprint.route('/violations/<int:violation_number>')
def show_single_violation(violation_number):
    violation = Violations.query.options(db.joinedload('inspection')).get(violation_number)
    return render_template('violations/single-violation.html' ,violation=violation)