from flask import *
from ConfigReader import get_mysql_config
from mysql_orm import *


app = Flask(__name__)

# 初始化MySQL
MYSQL_CONFIG = get_mysql_config()
MYSQL_USER = MYSQL_CONFIG['MYSQL_USER']
MYSQL_PASSWORD = MYSQL_CONFIG['MYSQL_PASSWORD']
MYSQL_HOST = MYSQL_CONFIG['MYSQL_HOST']
MYSQL_DB = MYSQL_CONFIG['MYSQL_DB']
MYSQL_URI = 'mysql://' + MYSQL_USER + ':' + MYSQL_PASSWORD + '@' + MYSQL_HOST + '/' + MYSQL_DB
app.config["SQLALCHEMY_DATABASE_URI"] = MYSQL_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config["SQLALCHEMY_ECHO"] = False
db.init_app(app)


@app.route('/')
def index_page():
    return send_file('pages/login/login.html')


# TODO 登录页模块
from pages.login.login import login
app.register_blueprint(login, url_prefix='/login')

# TODO 注册页
from pages.register.register import register
app.register_blueprint(register, url_prefix='/register')


# TODO admin管理页
from pages.admin.admin import admin
app.register_blueprint(admin, url_prefix='/admin')

# TODO 主页模块
from pages.home.home import home
app.register_blueprint(home, url_prefix='/home')

# TODO 历史值查询模块
from pages.history.history import history
app.register_blueprint(history, url_prefix='/history')

# TODO 阈值设定页面
from pages.threshold.threshold import threshold
app.register_blueprint(threshold,  url_prefix='/threshold')

# TODO 警报查看
from pages.alarm.alarm import alarm
app.register_blueprint(alarm,  url_prefix='/alarm')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)
