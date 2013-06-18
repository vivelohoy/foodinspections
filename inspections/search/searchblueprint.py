import requests, json
from datetime import datetime
from flask import Blueprint, render_template, request
from inspections import db
from inspections.models.models import Branches, Facilities, Violations, Inspection, InspectionComments

search_blueprint = Blueprint("search_blueprint", __name__)




def search_zip(search):
    try:
        if int(search.replace('%', '')) and len(search.replace('%', '')) == 5:
            all_results = {}
            search_results = Facilities.query.filter(Facilities.zip.like(search))
            all_results['facilities'] = search_results.all()
            print "returning"
            return all_results

    except ValueError:
        return


@search_blueprint.route("/search", methods=['POST', 'GET'])
def search():
    if request.method == 'POST':
        if request.form['main-data']:
            original_search = request.form['main-data']
            length_of_search = len(original_search)

            if length_of_search <= 3: # Query too big to perform on sane time
                return render_template('search/no-search.html')

            search_keyword = request.form['main-data'].replace('\'', '').replace('"', '').replace('<', '').replace('>', '')
            search_keyword = '%' + search_keyword + '%'
            all_results = {}

            search_results = Branches.query.filter(Branches.branch_name.like(search_keyword))
            search_comments_results = InspectionComments.query.filter(InspectionComments.comment.like(search_keyword))

            all_results['branches'] = search_results.all()
            all_results['comments'] = search_comments_results.all()
            if all_results['branches'] or all_results['comments']:
                return render_template('search/results.html', results=all_results, searched=original_search)
                
            else:
                zip_codes = search_zip(search_keyword)
            
                if zip_codes:
                    return render_template('search/results.html', results=zip_codes, searched=original_search)
        else: 
            return render_template('search/no-search.html')
    else:
        return render_template('search/no-search.html')
