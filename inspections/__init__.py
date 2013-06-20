from flask import Flask, render_template
from flask.ext.sqlalchemy import *
from flask.ext.restless import APIManager

application = Flask(__name__)

application.config.from_object('config')

db = SQLAlchemy(application)
manager = APIManager(application, flask_sqlalchemy_db=db)

@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@application.template_filter('startswith')
def startswith_filter(s, l):
    return s.startswith(l)

from inspections.violations.violationsblueprint import violations_blueprint
from inspections.inspection.inspection import inspection_blueprint
from inspections.branch.branchblueprint import branch_blueprint
from inspections.resources.resourcesblueprint import resources_blueprint
from inspections.search.searchblueprint import search_blueprint
from inspections.home.homeblueprint import home_blueprint
from inspections.facility.facilityblueprint import facility_blueprint

application.register_blueprint(violations_blueprint)
application.register_blueprint(inspection_blueprint)
application.register_blueprint(branch_blueprint)
application.register_blueprint(resources_blueprint)
application.register_blueprint(search_blueprint)
application.register_blueprint(home_blueprint)
application.register_blueprint(facility_blueprint)

if __name__ == '__main__':
    application.run()
