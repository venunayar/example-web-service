import logging
from datetime import datetime

from utils.sharedState import SharedState

from models import libraries, users


def add_and_commit_db(db, entries):
    try:
        for entry in entries:
            db.session.add(entry)
            db.session.commit()
    except Exception as e:
        logging.getLogger(__name__).exception(e)
        db.session.rollback()
        return

def create_default_account_info(db):
    user_manager = SharedState().getInstance().user_mgr
    admin_role = users.Role(name="ADMIN")
    user_role = users.Role(name="USER")
    default_admin = users.User(username='admin',
        password=user_manager.hash_password('admin'),
        fullname='admin',
        email='admin@nayar.org',
        is_active=True,
        confirmed_at=datetime.utcnow(), roles=[admin_role])

    default_library = libraries.Library(name='default_library',
        admin='admin',
        is_active=True,
        users=[default_admin])
    add_and_commit_db(db, [default_library, admin_role, user_role])
    return

def create_default_entries_in_db(db=None):
    db = db if db else SharedState().getInstance().db
    create_default_account_info(db)
    return
