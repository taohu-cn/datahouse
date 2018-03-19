# -*- coding: utf-8 -*-
# __author__: taohu

from flask import Blueprint

api = Blueprint('api', __name__)

from . import views
