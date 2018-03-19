# -*- coding: utf-8 -*-
# __author__: taohu

from flask import Blueprint

app01 = Blueprint('app01', __name__)

from . import views
