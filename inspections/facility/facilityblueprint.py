from string import ascii_uppercase
from flask import Blueprint, render_template, redirect, url_for, Response
from inspections.models.models import *

facility_blueprint = Blueprint("facility_blueprint", __name__)

@facility_blueprint.route("/facility/<url_name>")
def show_facility(url_name):
    data = Facilities.query.filter_by(url_name=url_name).first_or_404()
    return render_template("facility/single-facility.html", facility=data )
