import os
import sys
import datetime
import time
import logging
import logging.config
import gzip
from utils.shared_state import SharedState
import lms


class DisableLogging(object):
    def __init__(self, loggers=None):
        loggers = [''] if loggers is None else loggers
        self.loggers = [{'logger': logging.getLogger(l), 'old_level': logging.getLogger(l).level} for l in loggers]

    def __enter__(self):
        for l in self.loggers:
            [h.acquire() for h in l['logger'].handlers]
            l['logger'].setLevel(logging.WARNING)

    def __exit__(self, et, ev, tb):
        for l in self.loggers:
            l['logger'].setLevel(l['old_level'])
            [h.release() for h in l['logger'].handlers]
        # implicit return of None => don't swallow exceptions

class ModuleFuncFilter(logging.Filter):
    def filter(self, record):
        record.module_funcname = '%s.%s' % (record.name, record.funcName)
        return True


class UTCFormatter(logging.Formatter):
    converter = time.gmtime

ONE_MB = (1024*1024)
class LmsFileHandler1(logging.handlers.RotatingFileHandler):
    def __init__(self, filename=None, maxBytes=ONE_MB, backupCount=20):
        pathname = os.path.join(os.environ['LMS_BASE'], lms.Config.LOG_FOLDER)
        filename = os.path.join(pathname, filename)
        self.rotator = self.rotator
        self.namer = self.namer
        super(LmsFileHandler1, self).__init__(filename, maxBytes=maxBytes, backupCount=backupCount)

    @staticmethod
    def rotator(source, dest):
        with open(source, "rb") as sf:
            data = sf.read()
            with gzip.open(dest, "wb") as df:
                df.write(data)
        os.remove(source)

    @staticmethod
    def namer(name):
        return name + ".gz"


class LmsFileHandler(logging.handlers.WatchedFileHandler):
    def __init__(self, filename=None):
        pathname = os.path.join(os.environ['LMS_BASE'], lms.Config.LOG_FOLDER)
        filename = os.path.join(pathname, filename)
        super(LmsFileHandler, self).__init__(filename)

def setup_flask_logger(app):
    l = logging.getLogger()
    for h in l.handlers:
        app.logger.addHandler(h)
    app.logger.setLevel(l.level)
    app.logger.addFilter(ModuleFuncFilter())
    if not app.config['LOG_TO_STDERR']:
        app.logger.disabled = 1

def backup_existing_logs():
    pathname = os.path.join(os.environ['LMS_BASE'], lms.Config.LOG_FOLDER)
    if os.path.isdir(pathname):
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d-%H_%M_%S")
        newpathname = pathname + '-' + timestamp
        os.rename(pathname, newpathname)
    os.makedirs(pathname)

import time

def setup_logger():
    try:
        app = SharedState().getInstance().app
        setup_flask_logger(app)
    except Exception as e:
        print e
        raise e

LMS_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'lms': {
            '()': ModuleFuncFilter,
        }
    },
    'formatters': {
        'lms': {
            '()': UTCFormatter,
            'format': '%(asctime)-15s %(levelname)-8s %(module_funcname)-50.50s: %(message)s [%(filename)s: %(lineno)d]',
        },
        'lmsaccess': {
            '()': UTCFormatter,
            'format': '%(asctime)-15s %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'level': 'DEBUG',
            'filters': ['lms',],
            'formatter': 'lms',
        },
        'logfile': {
            'class': 'cfg.logconf.LmsFileHandler',
            'filename': 'lms.log',
            'level': 'DEBUG',
            'formatter': 'lms',
            'filters': ['lms',],
        },
    },
    'root': {
        'handlers': ['console','logfile'],
        'level': 'DEBUG',
    }
}
