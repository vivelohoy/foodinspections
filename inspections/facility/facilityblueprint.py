from string import ascii_uppercase
from flask import Blueprint, render_template, redirect, url_for, Response
from inspections.models.models import *

facility_blueprint = Blueprint("facility_blueprint", __name__)

@facility_blueprint.route("/facility/<facility_name>/<address>")
def show_facility(facility_name, address):
    data = Facilities.query.get((str(facility_name),str(address)))
    return render_template("facility/single-facility.html", facility=data )
