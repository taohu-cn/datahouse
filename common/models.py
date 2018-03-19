# -*- coding: utf-8 -*-
# __author__: taohu

from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import relationship
from sqlalchemy.types import String, Integer, DateTime
import datetime
from run import db

"""
<> Python Console
>>> from common.models import db
>>> db.create_all()
"""


class Project(db.Model):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), server_default='', nullable=False)
    type = Column(String(50), server_default='', nullable=False)
    pro_uid = Column(String(50), server_default='', nullable=True)
    pm = Column(String(50), server_default='', nullable=True)
    op = Column(String(50), server_default='', nullable=True)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    def __repr__(self):
        return '<Name %r>' % self.name


class Instance(db.Model):
    __tablename__ = 'instance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String(50), server_default='', nullable=False)
    port = Column(String(50), server_default='', nullable=False)
    db_usage = Column(String(50), server_default='', nullable=False)
    db_type = Column(String(50), server_default='', nullable=False)
    create_time = Column(DateTime, index=True, default=datetime.datetime.now, nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), index=True)
    project_obj = relationship('Project', lazy='joined', cascade='all')


class Size(db.Model):
    __tablename__ = 'size'
    id = Column(Integer, primary_key=True, autoincrement=True)
    size = Column(String(50), server_default='', nullable=False)
    tactics = Column(String(8), nullable=False)
    time_cost = Column(String(8), nullable=False)
    agent_date = Column(String(16), server_default=datetime.datetime.now().strftime('%Y-%m-%d'), nullable=False)
    agent_datetime = Column(String(16), server_default=datetime.datetime.now().strftime('%Y-%m-%d'), nullable=False)
    create_time = Column(DateTime, index=True, default=datetime.datetime.now, nullable=False)
    instance_id = Column(Integer, ForeignKey('instance.id'), index=True)
    instance_obj = relationship('Instance', lazy='joined', cascade='all')
