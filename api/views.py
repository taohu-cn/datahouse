# -*- coding: utf-8 -*-
# __author__: taohu

import datetime
import json
from flask import request
from sqlalchemy import and_
from common.models import Project, Instance, Size
from run import db
from . import api

OFFERSET_DAYS = datetime.timedelta(days=50)


def time_market(flag):
    current_date = datetime.date.today()
    start_date = (current_date - OFFERSET_DAYS).strftime("%Y-%m-%d")

    if flag == "CD":
        return current_date
    elif flag == "SD":
        return start_date


@api.route('/data/instances/', methods=['GET'])
def data_instance():
    pro_id = request.args.get('pro_id')
    if pro_id:
        # print(pro_id)
        res_obj = db.session.query(Instance).filter(Instance.project_id == pro_id)
    else:
        # print('all')
        res_obj = db.session.query(Instance).all()

    tmp_list = []
    for i in res_obj:
        tmp_dict = {"id": i.id, "host": i.host, "port": i.port, "db_usage": i.db_usage}
        tmp_list.append(tmp_dict)
    return json.dumps(tmp_list)


@api.route('/data/size/', methods=['GET'])
@api.route('/data/size/<uid>/', methods=['GET'])
def data_get_size(uid):
    data_dic = {
        "date": [],
        "datetime": [],
        "size": []
    }
    sd = time_market("SD")
    pick_date = datetime.date(int(sd.split("-")[0]), int(sd.split("-")[1]), int(sd.split("-")[2]))
    while pick_date <= time_market("CD"):
        pick_res = db.session.query(Size).filter(and_(Size.instance_id == uid), Size.agent_date == pick_date).all()
        if pick_res:
            for i in pick_res:
                data_dic["date"].append(str(i.agent_date))
                data_dic["datetime"].append(str(i.agent_datetime))
                data_dic["size"].append(i.size)
        else:
            data_dic["date"].append(str(pick_date))
            data_dic["datetime"].append("0")
            data_dic["size"].append("0")

        pick_date += datetime.timedelta(days=1)

    # res = db_session.query(Size).filter(and_(Size.instance_id == uid), Size.agent_date > time_market("SD")).all()
    # for i in res:
    #     data_dic["date"].append(str(i.agent_date))
    #     data_dic["datetime"].append(str(i.agent_datetime))
    #     data_dic["size"].append(i.size)
    #
    # last_date_list = data_dic["date"][-1].split("-") if data_dic["date"] else time_market("SD").split("-")
    # last_date = datetime.date(int(last_date_list[0]), int(last_date_list[1]), int(last_date_list[2]))
    #
    # while last_date < time_market("CD"):
    #     last_date = last_date + datetime.timedelta(days=1)
    #     data_dic["date"].append(str(last_date))
    #     data_dic["size"].append(0)

    return json.dumps(data_dic)
