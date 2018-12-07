from flask import Flask
from flask_user import SQLAlchemyAdapter, UserManager

from cfg import logconf
from models import users


def user_config():
    db = SharedState().getInstance().db
    app = SharedState().getInstance().app

    db_adapter = SQLAlchemyAdapter(db, users.User)
    user_manager = UserManager(db_adapter, app)
    SharedState().getInstance().user_mgr = user_manager
    logging.getLogger(__name__).info('Finished Initializing flask_user')

class FlaskInit(object):
    def __init__(self):
        self.flask_app = Flask(__name__)
        logconf.setup_logger()
        user_config()

    def get_flask_app(self):
        return self.flask_app


flask_init = FlaskInit()
leitrim_server = flask_init.get_flask_app()
leitrim_server.run(host='0.0.0.0', port=5002)
