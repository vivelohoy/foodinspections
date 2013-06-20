from flask import Blueprint, render_template, redirect, url_for, make_response, request
from inspections.models.models import *

inspection_blueprint = Blueprint("inspection_blueprint", __name__)

@inspection_blueprint.route('/api/static/<query>')
def return_data(query):
    query = query.lower()
    if query == 'latest':
        inspections = Inspection.query.order_by(Inspection.inspection_date.desc()).limit(100).all()
    elif query == 'failed':
        inspections = Inspection.query.filter_by(results='Fail').order_by(Inspection.inspection_date.desc()).limit(100).all()
    elif query == 'passed':
        inspections = Inspection.query.filter_by(results='Pass').order_by(Inspection.inspection_date.desc()).limit(100).all()
    else: inspections = None
    resp = make_response(render_template('inspection/inspectionjson.html', inspections=inspections))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@inspection_blueprint.route('/inspections')
def inspection_data():
    r = request.args.get('r')
    if not r:
        r = ""
    return render_template('inspection/inspection-table.html', param=r)

@inspection_blueprint.route('/inspections/<id>')
def show_inspection(id):
    return (render_template('inspection/single-inspection.html', inspection=Inspection.query.get_or_404(id)))
