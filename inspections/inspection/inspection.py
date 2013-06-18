from flask import Blueprint, render_template, redirect, url_for, make_response
from inspections.models.models import *

INSPECTIONS_PER_PAGE = 100
inspection_blueprint = Blueprint("inspection_blueprint", __name__)

@inspection_blueprint.route('/api/data')
def return_data():
    inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).limit(100).all()
    resp = make_response(render_template('inspection/inspectionjson.html', inspections=inspections))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@inspection_blueprint.route('/inspections')
def inspection_data():
    return render_template('inspection/inspection-table.html')

@inspection_blueprint.route('/inspections/<id>')
def show_inspection(id):
    return (render_template('inspection/single-inspection.html', inspection=Inspection.query.get_or_404(id)))

