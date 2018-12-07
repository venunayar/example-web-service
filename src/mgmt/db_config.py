import importlib
import logging

from utils.sharedState import SharedState


def _import_base_module(model_module=None):
    return importlib.import_module('{}.base'.format(model_module))


def db_init(model_module=None):
    db = SharedState().getInstance().db
    app = SharedState().getInstance().app
    db.app = app
    db.init_app(app)
    base = _import_base_module(model_module)
    db.register_base(base.LeitrimBase)
    db.session.commit()
    logging.getLogger(__name__).info('Finished Initializing flask-alchemy')
    return


def db_create(db=None):
    db = SharedState().getInstance().db if not db else db
    from sqlalchemy_utils import database_exists, create_database
    if not database_exists(db.engine.url):
        logging.getLogger(__name__).info('Start creating database: {}'.format(db.engine.url))
        create_database(db.engine.url, encoding='latin1')
        db.session.commit()
        logging.getLogger(__name__).info('Finished creating database: {}'.format(db.engine.url))
    return


def db_create_tables(db=None, model_module=None):
    db = SharedState().getInstance().db if not db else db
    logging.getLogger(__name__).info('Start creating tables: {}'.format(db.engine.url))
    base = _import_base_module(model_module)
    base.LeitrimBase.metadata.create_all(bind=db.engine)
    db.session.commit()
    logging.getLogger(__name__).info('Finished creating tables: {}'.format(db.engine.url))
    return


def db_delete_tables(db=None, model_module=None):
    db = SharedState().getInstance().db if not db else db
    logging.getLogger(__name__).info('Start dropping tables: {}'.format(db.engine.url))
    base = _import_base_module(model_module)
    base.LeitrimBase.metadata.drop_all(bind=db.engine)
    logging.getLogger(__name__).info('Finished dropping tables: {}'.format(db.engine.url))
    return


def db_delete(db=None):
    db = SharedState().getInstance().db if not db else db
    from sqlalchemy_utils import database_exists, drop_database
    if database_exists(db.engine.url):
        logging.getLogger(__name__).info('Start dropping database: {}'.format(db.engine.url))
        drop_database(db.engine.url)
        logging.getLogger(__name__).info('Finished dropping database: {}'.format(db.engine.url))
    return
