# -*- coding: utf-8 -*-
# __author__: taohu


from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from common import generate

# SQLALCHEMY_DATABASE_URI = 'mysql://datahouse:datahouse@172.16.81.62:23006/datahouse?charset=utf8'


def app_framework():
    appx = Flask(__name__)
    appx.config.from_object(generate)

    from base import root
    appx.register_blueprint(root, url_prefix='/')

    # from api import api
    # appx.register_blueprint(api, url_prefix='/api')

    from app01 import app01
    appx.register_blueprint(app01, url_prefix='/app01')

    return appx


app = app_framework()
db = SQLAlchemy(app)

if __name__ == '__main__':
    app.run()
