from datetime import datetime

from flask import Blueprint, current_app
from APP.models import *
import pandas as pd
def addSimpleData():
    data = pd.read_csv('APP/static/Sample1000.csv')
    if data.empty:
        return
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
                print('添加成功',activity)
            except Exception as e:
                print(e)


addSimpleData()