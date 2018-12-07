from flask import Flask
from flask_user import SQLAlchemyAdapter, UserManager

from cfg import logconf
from db_config import db_create, db_create_tables, db_delete
from init_db import create_default_entries_in_db
from models import users


def user_config():
    db = SharedState().getInstance().db
    app = SharedState().getInstance().app

    user_manager = UserManager(app, db, users.User)
    SharedState().getInstance().user_mgr = user_manager
    logging.getLogger(__name__).info('Finished Initializing flask_user')

class FlaskInit(object):
    def __init__(self):
        self.flask_app = Flask(__name__)
        logconf.setup_logger()
        user_config()

    def db_setup(self, default_entry_create=True):
        # once we start migrations, we'll not do this
        db_delete()
        db_create()
        db_create_tables(model_module=self.model_module)
        if default_entry_create:
            create_default_entries_in_db()

    def get_flask_app(self):
        return self.flask_app


flask_init = FlaskInit()
leitrim_server = flask_init.get_flask_app()
leitrim_server.run(host='0.0.0.0', port=5002)
