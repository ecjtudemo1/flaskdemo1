from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager  #?????????????????????????????????????/
from flask_login import login_required
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:UMR123..@localhost/flask_demo3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = '44694a31fa044b51872d67344966a742'
db = SQLAlchemy(app)
#管理员表

class User(UserMixin, db.Model):
    __tablename__ = "user" # 表名为user，管理员
    id = db.Column(db.Integer, primary_key=True)#定义主键id
    name = db.Column(db.String(100), unique=True)#定义管理员name， 并设置为唯一
    password_hash = db.Column(db.String(100))#定义管理员的密码
    account_number = db.Column(db.String(100), unique=True)#定义管理员账号
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):   #用于生成密码的散列值，设置密码是要使用此函数，不能直接给password_hash赋值
        self.password_hash = generate_password_hash(password)
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)  #对密码进行散列化保密
    def __repr__(self):
        return "User %r" % self.name#返回表中的name值
@login_manager.user_loader#登录的函数
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/secret')
@login_required
def secret():   #保护路由，如果未认证的用户访问就返回到登录页面
    return 'your are not the user!'



#货余量表
class huowuliang(db.Model):
    __tablename__ = "huoyuliang"#定义表名为货余量
    id = db.Column(db.Integer, primary_key=True)#定义主键
    huowu_name = db.Column(db.String(100), unique=True)#定义货物的名称
    huowu_number = db.Column(db.String(100))#定义货物的余量

    def __repr__(self):
        return "huoyuliang %r" % self.huowu_name
#日监控数据表
class daily_monitor(db.Model):
    __tablename__ = "daily_monitor"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(100))
    sales_amount = db.Column(db.String(100))

    def __repr__(self):
        return "daily_monitor %r" % self.date
#if __name__ == '__main__':

    #us1 = User(name='wyy', account_number='wyy')
    #us1.password = '123456'
    #db.session.add_all([us1])
    #db.session.commit()








