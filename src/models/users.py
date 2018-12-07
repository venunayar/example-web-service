import datetime

from base import LmsBase
from flask_user import UserMixin
from json_mixin import OutputMixin
from sqlalchemy import Column
from sqlalchemy import DateTime, Integer, String, Boolean
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import backref, relationship

import cfg.lms_constants as lms_constants


class User(OutputMixin, LmsBase, UserMixin):
    username = Column(String(lms_constants.MAX_USERNAME_LENGTH), nullable=False)
    password = Column(String(lms_constants.MAX_PASSWORD_LENGTH), nullable=False, default='')
    email = Column(String(lms_constants.MAX_EMAIL_LENGTH), nullable=False)

    # flask user stuff
    reset_password_token = Column(String(100), nullable=False, default='')
    confirmed_at = Column(DateTime, nullable=False, default=datetime.datetime.now)
    is_active = Column(Boolean(name='ck_user_is_active'), nullable=False, default=False)

    # flask user relationships
    roles = relationship('Role', secondary='userroles', backref=backref('user', lazy='dynamic'))

    fullname = Column(String(lms_constants.MAX_STRING_LENGTH), default='')
    isadmin = Column(Boolean(name='ck_user_isadmin'), default=False)

    # user parent relationships
    library_id = Column(Integer, ForeignKey('library.id')) # M:1

    UniqueConstraint(username)
    def __unicode__(self):
        return "<User(id={}, username={}, library_id={})>".format(self.id, self.username, self.library_id) or ''

class Role(OutputMixin, LmsBase):
    name = Column(String(lms_constants.MAX_STRING_LENGTH), nullable=False, unique=True)

    def __unicode__(self):
        return "<Role(id={}, name={})>".format(self.id, self.name) or ''

class UserRoles(OutputMixin, LmsBase):
    user_id = Column(Integer(), ForeignKey('user.id', ondelete='CASCADE'))
    role_id = Column(Integer(), ForeignKey('role.id', ondelete='CASCADE'))

    def __unicode__(self):
        return "<UserRoles(id={}, user_id={}, role_id={})>".format(self.id, self.user_id, self.role_id) or ''


