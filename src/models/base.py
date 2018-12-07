import datetime
import logging
import uuid

from cfg.lms_constants import MAX_STRING_LENGTH
from sqlalchemy import DateTime, Integer, String
from sqlalchemy import MetaData, Column
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.ext.declarative import as_declarative, declared_attr

meta = MetaData(naming_convention={
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "%(table_name)s"
      })

def get_uuid():
    return uuid.uuid4().hex

def default_uuid(context):
    try:
        return '_'.join([context.compiled.statement.table.name, get_uuid()])
    except Exception as e:
        logging.getLogger(__name__).exception(e)


@as_declarative(metadata=meta)
class LmsBase(object):
    @declared_attr
    def __tablename__(self):
        return self.__name__.lower()
    @declared_attr
    def __table_args__(self):
        return PrimaryKeyConstraint(self.id),

    id = Column(Integer, autoincrement=True)
    uuid = Column(String(MAX_STRING_LENGTH), unique=True, nullable=False, default=default_uuid)
    created_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    updated_at = Column(DateTime, nullable=False, default=datetime.datetime.now, onupdate=datetime.datetime.now)


