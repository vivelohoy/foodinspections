import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
SQLALCHEMY_ECHO=True

if 'RDS_HOSTNAME' in os.environ:
    SQLALCHEMY_DATABASE_URI = 'mysql://' + os.environ['RDS_USERNAME'] + ':' + os.environ['RDS_PASSWORD'] +'@' + os.environ['RDS_HOSTNAME']  + '/' + os.environ['RDS_DB_NAME']
   
else:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'inspections.db')

THREADS_PER_PAGE = 8
