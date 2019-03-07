from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from flask_script import Shell, Manager

app = Flask(__name__)
manager = Manager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:UMR123..@localhost/flask_demo3'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

#第一个参数是Flask的实例，第二个参数是Sqlalchemy数据库实例
migrate = Migrate(app, db)

#manager是Flask-Script的实例，这条语句在flask-Script中添加一个db命令
manager.add_command('db', MigrateCommand)

class huowuliang(db.Model):
    __tablename__ = "huoyuliang"#定义表名为货余量
    id = db.Column(db.Integer, primary_key=True)#定义主键
    huowu_name = db.Column(db.String(100), unique=True)#定义货物的名称
    huowu_number = db.Column(db.String(100))#定义货物的余量

    def __repr__(self):
        return "huoyuliang %r" % self.huowu_name

