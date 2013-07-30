from inspections import db
from inspections import manager

inspection_violations = db.Table('inspection_violations',
    db.Column('violation_id', db.Integer, db.ForeignKey('violations.violation_number')),
    db.Column('inspection_id', db.Integer, db.ForeignKey('inspection.inspection_id')),
)

BRANCH_NAME_LEN = 100
FACILITY_NAME_LEN = BRANCH_NAME_LEN
ADDRESS_LEN = 100

class Branches(db.Model):
    branch_name = db.Column(db.String(BRANCH_NAME_LEN), primary_key=True)
    facilities = db.relationship('Facilities', backref='branches', lazy='dynamic')
    url_name = db.Column(db.String(FACILITY_NAME_LEN + ADDRESS_LEN), unique=True)

    def __init__(self, branch_name):
        self.branch_name = branch_name

class Facilities(db.Model):
    facility_name = db.Column(db.String(FACILITY_NAME_LEN), primary_key=True)
    url_name = db.Column(db.String(FACILITY_NAME_LEN + ADDRESS_LEN), unique=True)
    address = db.Column(db.String(ADDRESS_LEN), primary_key=True)
    aka_name = db.Column(db.String(FACILITY_NAME_LEN))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    zip_code = db.Column(db.Integer)
    state = db.Column(db.String(5))
    city = db.Column(db.String(15))
    license = db.Column(db.Integer)
    facility_type = db.Column(db.String(30))
    inspections = db.relationship('Inspection', backref='facilities', lazy='dynamic')
    branch_id = db.Column(db.String(BRANCH_NAME_LEN), db.ForeignKey('branches.branch_name'))
    
    def __init__(self, facility_name, address):
        self.facility_name = facility_name
        self.address = address
        

class Violations(db.Model):
    violation_number = db.Column(db.Integer, primary_key=True)
    details = db.Column(db.Text)
    def __init__(self, violation_number, details):
        self.violation_number = violation_number
        self.details = details 

        
class Inspection(db.Model):
    inspection_id = db.Column(db.Integer, primary_key=True)
    risk = db.Column(db.String(17))
    inspection_date = db.Column(db.DateTime)
    inspection_type = db.Column(db.String(50))
    results = db.Column(db.String(25))
    violations_count = db.Column(db.Integer)
    violations = db.relationship('Violations', secondary=inspection_violations, backref=db.backref('inspection', lazy='dinamic'))
    facility_id = db.Column(db.String(FACILITY_NAME_LEN), db.ForeignKey('facilities.facility_name'))
    facility_url_name = db.Column(db.String(FACILITY_NAME_LEN + ADDRESS_LEN))
    comments = db.relationship('InspectionComments', backref='inspection', lazy='dinamic')
    
    def __init__(self, inspection_id):
        self.inspection_id = inspection_id

        
class InspectionComments(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    comment = db.Column(db.Text)
    inspection_id = db.Column(db.Integer, db.ForeignKey('inspection.inspection_id'))
    
    def __init__(self, comment):
        self.comment = comment
        
api_inspection_blueprint = manager.create_api(Inspection, methods=['GET'], results_per_page=100, exclude_columns=['facilities','comments', 'violations'])

api_violations_blueprint = manager.create_api(Violations, methods=['GET'], results_per_page=50, exclude_columns=['inspection'])

api_branches_blueprint = manager.create_api(Branches, methods=['GET'])

api_facilities_blueprint = manager.create_api(Facilities, methods=['GET'], results_per_page=50, include_columns=['latitude','facility_name','longitude', 'address','inspections', 'facility_type', 'branch_id', 'zip_code','license','inspections.results'])

api_comments_blueprint = manager.create_api(InspectionComments, methods=['GET'])

api_branches_names_blueprint = manager.create_api(Facilities, methods=['GET'], exclude_columns=[], collection_name='facility_names', results_per_page=None)
