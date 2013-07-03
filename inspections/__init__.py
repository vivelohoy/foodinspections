from flask import Flask, render_template, request
from flask.ext.sqlalchemy import *
from flask.ext.restless import APIManager
from logging import FileHandler
import logging
from flask.ext.cache import Cache


CACHE_TIMEOUT = 60 * 5

application = Flask(__name__)

application.config.from_object('config')

file_handler = FileHandler('search.log', )
file_handler.setLevel(logging.INFO)

application.logger.addHandler(file_handler)

db = SQLAlchemy(application)
manager = APIManager(application, flask_sqlalchemy_db=db)
cache = Cache(application)

@application.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@application.template_filter('startswith')
def startswith_filter(s, l):
    return s.startswith(l)

@application.before_request
def return_cached():
    # if GET and POST not empty
    if not request.values and not request.path.startswith('/static') and not request.path.startswith('/search'):
        response = cache.get(request.path)
        if response: 
            return response

@application.after_request
def cache_response(response):
    if not request.values and not request.path.startswith('/static') and not request.path.startswith('/search'):
        cache.set(request.path, response, timeout=CACHE_TIMEOUT)
    return response

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
