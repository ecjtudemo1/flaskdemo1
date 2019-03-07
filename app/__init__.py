from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail, Message
from flask_socketio import SocketIO#？？？？？？？？？？？？？？？？？？
app = Flask(__name__)
login_manager = LoginManager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)
db = SQLAlchemy(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['MAIL_USERNAME'] = '18970900848@163.com'
app.config['MAIL_PASSWORD'] = 'kangcheng61'
mail = Mail(app)
async_mode = None     # 新添加的代码？？？？？？？？？？？？？？？？？？？？？
socketio = SocketIO()
app.debug = True

from .main import main as main_blueprint
app.register_blueprint(main_blueprint)
socketio.init_app(app=app, async_mode=async_mode)#？？？？？？？？？？？？？？
#网站的功能：
# 1、记录并显示出每台售卖机的商品剩余数量（数据可视化分析）
       #（以下为一台售卖机）
       #1、通过表格写出剩余量
       #2、做出每种商品不同日期的折线图。
# 2、当剩余量底于一定值是发送邮件给管理员（邮件系统）
# 3、支付界面