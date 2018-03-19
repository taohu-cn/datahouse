# -*- coding: utf-8 -*-
# __author__: taohu

import datetime
import json
from flask import render_template, request
from sqlalchemy import and_
from common.models import Project, Instance, Size
from run import db
from . import app01

OFFERSET_DAYS = datetime.timedelta(days=50)


# START_DATE = (CURRENT_DATE - OFFERSET_DAYS).strftime("%Y-%m-%d")


def time_market(flag):
    current_date = datetime.date.today()
    start_date = (current_date - OFFERSET_DAYS).strftime("%Y-%m-%d")

    if flag == "CD":
        return current_date
    elif flag == "SD":
        return start_date


@app01.route('/show/dashboard/', methods=['GET'])
def dashboard():
    ins_obj = db.session.query(Instance).all()
    return render_template("web/dashboard.html", ins_obj=ins_obj)


@app01.route('/data/project/', methods=['GET'])
# @login_required
def project():
    pro_obj = db.session.query(Project).filter(2 > 1).order_by(Project.op)
    return render_template("web/project.html", pro_obj=pro_obj)


@app01.route('/data/instance/', methods=['GET'])
@app01.route('/data/instance/<uid>/', methods=['GET'])
def instance(uid):
    pro_name = db.session.query(Project.name).filter(Project.id == uid).all()
    ins_obj = db.session.query(Instance).filter(Instance.project_id == uid)
    return render_template("web/instance.html", pro_id=uid, pro_name=pro_name[0][0], ins_obj=ins_obj)


@app01.route('/data/instances/', methods=['GET'])
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


@app01.route('/data/instance/detail/')
@app01.route('/data/instance/detail/<uid>/')
def instance_detail(uid):
    size_res = db.session.query(Size).filter(
        and_(Size.instance_id == uid), Size.agent_date > time_market("SD")).order_by(-Size.agent_date)
    ins_obj = db.session.query(Instance).filter(Instance.id == uid).first()
    ins_title = ins_obj.db_usage + ' (' + ins_obj.host + ':' + ins_obj.port + ')'
    return render_template('web/instanceDetail.html', size_res=size_res, ins_id=uid, ins_title=ins_title)


def str_to_date(time_str):
    time_list = time_str.split("-")
    return datetime.date(int(time_list[0]), int(time_list[1]), int(time_list[2]))


@app01.route('/data/size/', methods=['GET'])
@app01.route('/data/size/<uid>/', methods=['GET'])
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


# agent 上传数据接口
@app01.route('/data/info/', methods=['POST', 'GET'])
def data_post():  # Python 2.7.8 验证可用
    if request.method == 'GET':
        return 'GET'

    post_data = json.loads(request.data)
    # table project
    pro_name = post_data.get('pro_name', 0)
    pro_type = post_data.get('pro_type', 0)
    pro_master = post_data.get('pro_master', 0)
    pro_operations = post_data.get('pro_operations', 0)
    # table instance
    db_usage = post_data.get('db_usage', 0)  # <type 'unicode'> /?/ db_usage.encode("utf-8")
    db_type = post_data.get('db_type', 0)
    # table size
    host = post_data.get('host', 0)
    port = post_data.get('port', 0)
    size = post_data.get('size', 0)
    tactics = post_data.get('tactics', 0)
    time_cost = post_data.get('time_cost', 0)
    agent_date = post_data.get('agent_date', 0)
    agent_datetime = post_data.get('agent_datetime', 0)

    # 把数据保存到 MySQL
    # 判定项目是否存在, 或新增
    pro_obj = db.session.query(Project).filter(and_(Project.name == pro_name), Project.type == pro_type).first()
    if not pro_obj:
        pro_obj = Project(name=pro_name, type=pro_type, pm=pro_master, op=pro_operations)
        db.session.add(pro_obj)
        db.session.flush()
    else:
        pro_obj.pm = pro_master
        pro_obj.op = pro_operations
        db.session.commit()

    # 判定实例是否存在, 或新增
    ins_obj = db.session.query(Instance).filter(
        and_(Instance.host == host),
        and_(Instance.port == port),
        Instance.project_id == pro_obj.id
    ).first()
    if not ins_obj:
        ins_obj = Instance(host=host, port=port, db_usage=db_usage, db_type=db_type, project_id=pro_obj.id)
        db.session.add(ins_obj)
        db.session.flush()
    else:
        ins_obj.db_usage = db_usage
        ins_obj.db_type = db_type
        ins_obj.project_id = pro_obj.id
        db.session.commit()

    # 添加新数据
    new_row_obj = Size(
        size=str(size),
        tactics=tactics,
        time_cost=time_cost,
        agent_date=agent_date,
        agent_datetime=agent_datetime,
        instance_id=ins_obj.id
    )

    db.session.add(new_row_obj)
    db.session.commit()
    return 'OK'
