from datetime import datetime

from flask import Blueprint, current_app
from .models import *
import pandas as pd
#绑定flask（app） url_prefix访问分权
blue=Blueprint('user',__name__,url_prefix='')

@blue.route('/')
def index():
    return 'hello'

@blue.route('/addSimpleData/')
def addSimpleData():
    data = pd.read_csv('APP/static/Sample1000.csv')
    # print(data)
    with current_app.app_context():
        for _, row in data.iterrows():
            # 创建 CleanupActivity 实例
            activity = debris(
                activity_id=row['id'],
                startdate=datetime.strptime(row['startdate'], '%d/%m/%Y %H:%M:%S'),  # 格式化日期时间
                county_name=row['county_name'],
                geom_wkt=row['geom_wkt'],
                kg_of_collected_waste=row['kg_of_collected_waste'],
                others=row['others'],
                hygiene=row['hygiene'],
                industrial=row['industrial'],
                fisheries=row['fisheries'],
                personal_use=row['personal_use']
            )
            try:
            # 将实例添加到数据库会话
                db.session.add(activity)
            # 提交会话以保存更改
                db.session.commit()
                return'success'
            except Exception as e:
                print(e)
                return 'fail'


@blue.route('/readData/')
def readData():
    debris_data = debris.query.all()
    return 'query success'+debris_data[0].geom_wkt

@blue.route('/upData/')
def upData():
    debris_data = debris.query.all()
    points=[]
    for data in debris_data:
        result_string = data.geom_wkt.replace("POINT", "").strip()
        data.geom_wkt = result_string
        points.append(data.geom_wkt)
    db.session.commit()
    return 'updata success'+points[11]

@blue.route('/upData2/')
def upData2():

    debris_data = debris.query.all()
    points=[]
    for data in debris_data:
        result_string = "POINT" + data.geom_wkt
        data.geom_wkt = result_string
        points.append(data.geom_wkt)
    db.session.commit()
    return 'updata success'+debris_data[0].geom_wkt