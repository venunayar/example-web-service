from sqlalchemy import Column
from base import LmsBase
from ip_network import IPNetworkType
from json_mixin import OutputMixin
from sqlalchemy import Column
from sqlalchemy import Integer, String, Boolean
from sqlalchemy import PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy_json import MutableJson

import cfg.lms_constants as lms_constants

class Library(OutputMixin, LmsBase):
    name = Column(String(lms_constants.MAX_STRING_LENGTH), nullable=False, unique=True)
    admin = Column(String(lms_constants.MAX_STRING_LENGTH), nullable=False)
    is_active = Column(Boolean(name='ck_library_is_active'), nullable=False, default=True)

    # library child relationships
    users = relationship('User', backref='library', cascade="all") # 1:M

    PrimaryKeyConstraint('id')
    def __unicode__(self):
        return "<Library(id={}, name={})>".format(self.id, self.name) or ''

