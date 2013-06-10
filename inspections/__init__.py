from flask import Flask, render_template
from flask.ext.sqlalchemy import *
from flask.ext.restless import APIManager

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)
manager = APIManager(app, flask_sqlalchemy_db=db)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.template_filter('startswith')
def startswith_filter(s, l):
    return s.startswith(l)

from inspections.violations.violationsblueprint import violations_blueprint
from inspections.inspection.inspection import inspection_blueprint
from inspections.branch.branchblueprint import branch_blueprint
from inspections.resources.resourcesblueprint import resources_blueprint
from inspections.search.searchblueprint import search_blueprint

app.register_blueprint(violations_blueprint)
app.register_blueprint(inspection_blueprint)
app.register_blueprint(branch_blueprint)
app.register_blueprint(resources_blueprint)
app.register_blueprint(search_blueprint)


if __name__ == '__main__':
    app.run()
