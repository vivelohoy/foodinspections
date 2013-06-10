from flask import Blueprint, render_template, redirect, url_for
from inspections.models.models import *
from inspections.violations.violationsblueprint import show_single_violation

INSPECTIONS_PER_PAGE = 100
inspection_blueprint = Blueprint("inspection_blueprint", __name__)


@inspection_blueprint.route('/')
@inspection_blueprint.route('/inspections')
def inspection_data():
    return render_template('inspection/inspection-table.html')

@inspection_blueprint.route('/inspections/<id>')
def show_inspection(id):
    return (render_template('inspection/single-inspection.html', inspection=Inspection.query.get_or_404(id)))

# @inspection_blueprint.route('/categories')
# @inspection_blueprint.route('/categories/<int:page>')
# def show_categories(page=1):
#     paginated_data = Inspection.query.paginate(page, per_page=INSPECTIONS_PER_PAGE)
#     data = Inspection.query.all()
#     categories = [] 
#     for record in data:
#         facility_category = record.facilities.facility_type
#         if facility_category in categories:
#             continue
#         else: categories.append(facility_category)
#     print categories
#     return render_template("inspection/inspection-categories.html", inspections=data, categories=categories)