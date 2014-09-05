import requests, json
from datetime import datetime
from inspections import *
from inspections.models.models import *
#from failedtweet import tweet_failed
from email_notify import send_email

API_ENDPOINT = "http://data.cityofchicago.org/resource/4ijn-s7e5.json"
API_LIMIT = 1000

def extract_string(data, data_query, keys):
	if data_query in keys:
		if data[data_query] != ',':
			return data[data_query]
	else: return "Unavailable"
	
def extract_int(data, data_query, keys):
	if data_query in keys:
		if data[data_query] != ',':
			return int(data[data_query])
	else: return None
	
def extract_date(data, data_query, keys):
	if data_query in keys:
		if data[data_query] != ',':
			date_segments = data[data_query].replace('T00:00:00', '').split('-')
			return datetime(int(date_segments[0]), int(date_segments[1]), int(date_segments[2]))
	else: return None
	
def extract_location(data, location_query, latitude_query, longitude_query, keys):
	if location_query in keys:
		if latitude_query in keys and longitude_query in keys:
			return (float(data[location_query][latitude_query]), float(data[location_query][longitude_query]))
		else: return (None, None)
	else: return (None, None)

def commas_clean(field):
	return field.replace(',', '').replace('  ', ' ')

def all_cap_to_sentence(text):
    return strip_capitalize(text) + "."
   
def all_cap_paragraph_to_formal(text):
    sentences = text.split(".")
    cleaned_sentences = []
    for sentence in sentences:
        cleaned_sentences.append(strip_capitalize(sentence) + ".")
    return " ".join(cleaned_sentences[:-2])

def strip_capitalize(word):
    return word.strip().lower().capitalize()

def branch_name_parser(dba_name):
    """Function to parse doing as business names to match more of them in the database"""
    dba_name = dba_name.lower()
    dba_name = dba_name.split("#")[0] # split on names like: My restaurant # 1221, and keep the My restaurant part
    dba_name = dba_name.split("@", 1)[0]
    dba_name = dba_name.replace("/", ' ') # to keep functional urls 
    dba_name = dba_name.replace("-", ' ') # for restaurants like 7-eleven
    dba_name = dba_name.replace("'", "") # Unfortunately needed in cases of Jimmy John's vs. Jimmy Johns
    dba_name = dba_name.replace("_", "")
    dba_name = dba_name.replace("llc", "")
    dba_name = dba_name.replace("org", "")
    dba_name = dba_name.replace("inc", "")
    dba_name = dba_name.replace("ltd", "")
    dba_name = dba_name.replace(".", "") 
    dba_name = dba_name.replace(",", "")
    dba_name = dba_name.replace("  ", "")
    # Format Text here
    dba_name = dba_name.title()
  
    # Finish it off
    dba_name = dba_name.strip()
    return dba_name


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return (False, instance)
    else:
        instance = model(**kwargs)
        return (True, instance)

def url_name_format(*fields):
    return '-'.join(' '.join(fields).split())

def update_create_inspection(record):
    record_keys = record.keys()
    
    branch_name = branch_name_parser(extract_string(record, 'dba_name', record_keys))
    new_branch, branch = get_or_create(db.session, Branches, branch_name=branch_name)
    if new_branch:
        branch.url_name = url_name_format(branch_name)
    
    facility_name = branch_name_parser(extract_string(record, 'dba_name', record_keys))
    address = extract_string(record, 'address', record_keys)
    address = ' '.join(word[0].upper() + word[1:].lower() for word in address.split())
    url_name = url_name_format(facility_name, address)
    new_facility, facility = get_or_create(db.session, Facilities, url_name=url_name)
    if new_facility:
        facility.aka_name = extract_string(record, 'aka_name', record_keys)
        facility.license = extract_int(record, 'license_', record_keys)
        facility.facility_type = strip_capitalize(extract_string(record, 'facility_type', record_keys))
        facility.latitude, facility.longitude = extract_location(record, 'location', 'latitude', 'longitude', record_keys)
        facility.zip_code = extract_int(record, 'zip', record_keys)
        facility.state = extract_string(record, 'state', record_keys)
        facility.city = strip_capitalize(extract_string(record, 'city', record_keys))
        facility.facility_name = facility_name
        facility.address = address
    
    inspection_id = extract_int(record, 'inspection_id', record_keys)
    new_inspection, inspection = get_or_create(db.session, Inspection, inspection_id=inspection_id)
    if new_inspection:
        inspection.risk = extract_string(record, 'risk', record_keys)
        inspection.inspection_date = extract_date(record, 'inspection_date', record_keys)
        inspection.inspection_type = extract_string(record, 'inspection_type', record_keys)
        inspection.results = extract_string(record, 'results', record_keys)
        inspection.facility_url_name = url_name
        inspection.facility_name = facility_name
    
    if 'violations' in record_keys:
        violation_list = record['violations'].split('|')
        all_violations = []
        all_comments = []
        seen_violations = []
        
        for violation in violation_list:
            comment_dictionary = {}
            comment_dictionary['comment_text'] = all_cap_paragraph_to_formal(violation.split('- Comments:', 1)[1])
            if comment_dictionary['comment_text'] != "":
                new_comment, comment = get_or_create(db.session, InspectionComments, comment=comment_dictionary['comment_text'])
                all_comments.append(comment)
            
            violation_dictionary = {}
            violation_dictionary['violation_number'] = violation.split('.', 1)[0].strip()
            violation_dictionary['details'] = all_cap_to_sentence(violation.split('.', 1)[1].split('- Comments:', 1)[0].strip())
            new_inspection_violation, inspection_violation = get_or_create(db.session, Violations, violation_number=violation_dictionary['violation_number'], details=violation_dictionary['details'])
            if inspection_violation.violation_number not in seen_violations:
                all_violations.append(inspection_violation)
                seen_violations.append(inspection_violation.violation_number)
                
        inspection.violations = all_violations
        inspection.comments = all_comments
        inspection.violations_count = len(all_violations)
    
    if inspection not in facility.inspections:
        facility.inspections.append(inspection)
    
    if facility not in branch.facilities:
        branch.facilities.append(facility)
    
    if new_inspection:
        db.session.add(inspection)
        #tweet_failed(inspection) uncommented for now until we pick a twitter username
    
    if new_facility:
        db.session.add(facility)
    
    if new_branch:
        db.session.add(branch)
    db.session.commit()

    if new_inspection
        print "Committed:", branch.branch_name, 'with facility:', facility.facility_name, facility.address, inspection.inspection_id

    return new_inspection

def scrape():
    parameters = {}
    parameters['$limit'] = 1000
    parameters['$offset'] = 0
    new_record_count = 0
    while (True):
        data = requests.get(API_ENDPOINT, params=parameters)
        if data.status_code != requests.codes.ok:
            return
        json_data = json.loads(data.content)
        if len(json_data) == 0:
            break
        parameters['$offset'] += 1000
        print "Fetched", data.url
        for record in json_data:
        new_inspection = update_create_inspection(record)
        if new_inspection:
            new_record_count += 1
        else: 
            print "Imported {0} new records.".format(new_record_count)
            send_email(to="Hoy Support <support@vivelohoy.com>",
                       _from=None,
                       subject="eatsafe.co Import: Imported {0} new records.".format(new_record_count),
                       body="eatsafe.co Import: Imported {0} new records.".format(new_record_count))            
            return

def create_db():
	db.create_all()

if __name__ == "__main__":
    scrape()
