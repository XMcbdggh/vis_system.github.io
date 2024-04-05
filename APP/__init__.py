from flask import Flask
from .view import blue
from .urls import *
from .exts import init_exts


def create_app():
    app = Flask(__name__)

    #注册蓝图
    app.register_blueprint(blueprint=blue)

    # 配置数据库
    db_url = 'mysql+pymysql://root:root@localhost:3306/Marine_debris?charset=utf8mb4'
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 禁止对象追踪修改


    #初始化
    init_exts(app)

    return app