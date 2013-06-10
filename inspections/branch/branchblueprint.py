from string import ascii_uppercase
from flask import Blueprint, render_template, redirect, url_for, Response
from inspections.models.models import *
branch_blueprint = Blueprint("branch_blueprint", __name__)
ABC = ascii_uppercase

@branch_blueprint.route("/branch/<branch_name>/")
def show_branch(branch_name):
    data = Branches.query.get_or_404(branch_name)
    return render_template("branch/single-branch.html", branch=data )

@branch_blueprint.route("/branch")
def show_branches():
    data = Branches.query.order_by(Branches.branch_name).all()
    return render_template("branch/all-branches.html", branches=data, abc=ABC)
