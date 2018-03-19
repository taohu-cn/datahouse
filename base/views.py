# -*- coding: utf-8 -*-
# __author__: taohu

from flask import render_template
from . import root


@root.route("/favicon.ico")
def get_favicon():
    return root.send_static_file("favicon.ico")


@root.route('/')
def hello_world():
    return render_template("root/index.html")


@root.route('/data_packet/')
def data_packet():
    return render_template("root/index.html")
