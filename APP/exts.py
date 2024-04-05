# exts.py:插件管理
# 扩展的第三方插件

#1、导包

from flask_sqlalchemy import SQLAlchemy  #ORM
from flask_migrate import Migrate  #数据库迁移
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
#2、初始化对象
db = SQLAlchemy() #ORM
migrate = Migrate() #数据迁移
api = Api()

# SWAGGER_TITLE = "API"
# SWAGGER_DESC = "API接口"
# # 地址，必须带上端口号
# SWAGGER_HOST = "http://127.0.0.1/:5000"
# swagger_config = Swagger.DEFAULT_CONFIG
# swagger_config["title"] = SWAGGER_TITLE
# swagger_config["description"] = SWAGGER_DESC
# swagger_config["host"] = SWAGGER_HOST
# Swagger=Swagger(config=swagger_config)
#3、和app对象绑定
def init_exts(app):
    db.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    CORS(app)
    # Swagger(app)