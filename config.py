import os
_basedir = os.path.abspath(os.path.dirname(__file__))

#DEBUG = True
#SQLALCHEMY_ECHO=True

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(_basedir, 'inspections.db')

THREADS_PER_PAGE = 8
