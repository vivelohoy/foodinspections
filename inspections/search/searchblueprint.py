import requests, json
from datetime import datetime
from inspections import application
from flask import Blueprint, render_template, request
from inspections import db
from inspections.models.models import Branches, Facilities, Violations, Inspection, InspectionComments
import datetime

search_blueprint = Blueprint("search_blueprint", __name__)

@search_blueprint.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        if request.form['main-data']:
            original_search = request.form['main-data']
            length_of_search = len(original_search)
            application.logger.info('Searched for: %s at %s' % (original_search, datetime.datetime.today()))
            if length_of_search <= 3: # Query too big to perform on sane time
                return render_template('search/no-search.html', response_message="Search term too short")
            search_keyword = request.form['main-data'].replace('\'', '').replace('"', '').replace('<', '').replace('>', '')
            search_keyword = '%' + search_keyword + '%'

            all_results = {}

            search_results = Branches.query.filter(Branches.branch_name.like(search_keyword))
            search_comments_results = InspectionComments.query.filter(InspectionComments.comment.like(search_keyword))

            all_results['branches'] = search_results.all()
            all_results['comments'] = search_comments_results.all()
            if all_results['branches'] or all_results['comments']:
                return render_template('search/results.html', results=all_results, searched=original_search)
                
            else: return render_template('search/no-search.html', response_message="No results found")
        else: 
            return render_template('search/no-search.html', response_message="No search keywords provided")
    else:
        return render_template('search/no-search.html', response_message="Search with the search bar above")
