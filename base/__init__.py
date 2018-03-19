# __author__: taohu

from flask import Blueprint

root = Blueprint('base', __name__)

from . import views
