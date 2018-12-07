import logging
from datetime import datetime

from utils.sharedState import SharedState
from utils.lms_exceptions import DbException

from models import libraries, users
from cfg import lms_cfg


def add_and_commit_db(db, entries):
    try:
        for entry in entries:
            db.session.add(entry)
            db.session.commit()
    except DbException as e:
        logging.getLogger(__name__).exception(e)
        db.session.rollback()
        return

def create_default_account_info(db):
    user_manager = SharedState().getInstance().user_mgr
    admin_role = users.Role(name="ADMIN")
    user_role = users.Role(name="USER")
    default_admin = users.User(username=lms_cfg.DEFAULT_LMS_ADMIN,
        password=user_manager.hash_password(lms_cfg.DEFAULT_LMS_PW),
        fullname=lms_cfg.DEFAULT_LMS_FN,
        email=lms_cfg.DEFAULT_LMS_EMAIL,
        is_active=True,
        confirmed_at=datetime.utcnow(), roles=[admin_role])

    default_library = libraries.Library(name=lms_cfg.DEFAULT_LMS_LIBRARY,
        admin=lms_cfg.DEFAULT_LMS_ADMIN,
        is_active=True,
        users=[default_admin])
    add_and_commit_db(db, [default_library, admin_role, user_role])
    return

def create_default_entries_in_db(db=None):
    db = db if db else SharedState().getInstance().db
    create_default_account_info(db)
    return
