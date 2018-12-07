'''
This file is used to generate configuration values for the lms.cfg
that are likely change for each server install.
'''

LMS_CFG_VERSION = 0.1

# database config
DB_HOST = ''
DB_USERNAME = ''
DB_PASSWORD = ''
SQLALCHEMY_DATABASE_URI = 'mysql://{}:{}@{}/Lms?charset=latin1'.format(DB_USERNAME, DB_PASSWORD, DB_HOST)

# LMS library and LMS library admin config
DEFAULT_LMS_LIBRARY = ''
DEFAULT_LMS_ADMIN = ''
DEFAULT_LMS_PW = ''
DEFAULT_LMS_EMAIL = ''
DEFAULT_LMS_FN = ''


