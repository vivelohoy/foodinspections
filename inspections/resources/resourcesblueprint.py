from flask import Blueprint, render_template

resources_blueprint = Blueprint("resources_blueprint", __name__)

@resources_blueprint.route("/resources")
def show_resources():
    return render_template("resources/resources.html")

