from . import main
from flask import render_template, redirect, url_for, flash, request, session
from datetime import datetime
from ..models import User
from flask import Flask
import json
import time
from app import socketio
from .forms import LoginForm
from flask_login import login_user, logout_user, login_required
from functools import wraps
from app import mail, Message
import pymysql
from threading import Lock
import random
app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '18970900848@163.com'
app.config['MAIL_PASSWORD'] = 'kangcheng61'
conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='UMR123..',
    db='flask_demo3',
    charset='utf8'
)

thread = None
thread_lock = Lock()
visitors_flowrate = ''
def background_thread(visitors_flowrate):
    while True:
        print(visitors_flowrate)
        visitors_flowrate = [str(random.randint(1, 100))]
        times = time.strftime('%H:%M:%S', time.localtime())
        socketio.sleep(5) # 每五秒发送一次
        socketio.emit('user_response', {'data': [times, visitors_flowrate]}, namespace='/websocket/user_refresh')
@socketio.on('connect', namespace='/websocket/user_refresh')
def connect():
    """ 服务端自动发送通信请求 """
    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread, (visitors_flowrate,))
    #emit('server_response', {'data': '试图连接客户端！'})


'''@socketio.on('connect_event', namespace='/websocket/user_refresh')
def refresh_message(message):
    """ 服务端接受客户端发送的通信请求 """
    emit('server_response', {'data': message['data']})'''



def admin_login_req(f):  #定义装饰器，用来限制登录
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session:
            return redirect(url_for("main.login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/', methods = ['GET'])
def index():
    a = request.get_data()#接收客户端发来的数据
    print(a)
    print(a[4])
    return render_template("index2.html", current_time = datetime.utcnow())

@main.route('/admin')
@admin_login_req
def admin(): #获取mysql中的数据并显示在admin.html中的表格
    cur = conn.cursor()
    sql = "select * from huoyuliang"
    cur.execute(sql)
    content = cur.fetchall()

    # 获取表头
    sql = "SHOW FIELDS FROM huoyuliang"
    cur.execute(sql)
    labels = cur.fetchall()
    labels = [l[0] for l in labels]
    #选取出货余量小于50的数据
    red_data = []
    num = 0
    for i in content:
        if int(i[2]) < 50:
            red_data.append(i)
    #判断邮件发送的条件，其中条件要改！！！！！！！！！！！！！！！！！！！！！1
    if len(red_data) > 2:
        if "mail" not in session:
            session['mail'] = 'warming'
            return redirect(url_for('.send_mail'))
        else:
            num = 1
    else:
        num = 2
    return render_template("admin.html", labels=labels, content=content, red_data=red_data, num=num)

@main.route('/login', methods = ['GET', 'POST'])
def login():    #登录视图函数
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(account_number = form.account.data).first()#form.data表示用户输入的数据的get
        if user is not None and user.verify_password(form.pwd.data):
            login_user(user, form.remember_me.data)
            session["user"] = form["account"]
            return redirect(request.args.get('next') or url_for('.index'))

        flash('密码或账号错误')


    return render_template('login.html', form = form)
@main.route('/logout')
@login_required
def logout():
    session.pop("user", None)
    session.pop("mail", None)
    logout_user()
    flash('you have been logged out!')
    return redirect(url_for('.index'))

@main.route('/mail') #定义发送邮寄的视图函数
def send_mail():
    msg = Message('你好', sender='18970900848@163.com', recipients=['1042162849@qq.com'])
    msg.body = '你好'#邮件的标题
    msg.html = '<b>售卖机现已缺货，请及时登入售卖机管理系统查看信息</b>' #邮件的内容        #要改！！！！！！！！！！！！
    mail.send(msg)
    return redirect(url_for('.admin'))

@main.route('/zhifu')
@admin_login_req
def zhifu():
    return redirect(url_for('.Commodity_management'))

@main.route('/huowu')
@admin_login_req
def huowuxinxi():
    return render_template('huowuxinxi.html')

@main.route('/data_get', methods=['POST'])#echarts异步加载数据视图函数
def my_echarts():
    cur = conn.cursor()
    sql = "select * from huoyuliang"
    cur.execute(sql)
    content = cur.fetchall()
    data = {}
    xday = []
    yvalue = []
    for i in content:
        xday.append(i[1])
        yvalue.append(i[2])
    data['xday'] = xday
    data['yvalue'] = yvalue
    j = json.dumps(data)
    return j

@main.route('/daily_monitor')
@admin_login_req
def daily_monitor():
    #获取日监控的数据？？？？？？？？？？？？？？？？？？？？？？？？
    return render_template('daily_monitor.html')

@main.route('/data_analysis')
@admin_login_req
def data_analysis():

    return render_template('data_analysis.html')


@main.route('/Data_visualization')
@admin_login_req
def Data_visualization():

    return render_template('Data_visualization.html')

@main.route('/Commodity_management')
@admin_login_req
def Commodity_management():

    return render_template('Commodity_management.html')
@main.route('/data_get1', methods=['POST'])#echarts异步加载折线图数据视图函数
def my_echart():
    cur = conn.cursor()
    sql = "select * from daily_monitor"
    cur.execute(sql)
    content = cur.fetchall()
    data = {}
    xday = []
    yvalue = []
    for i in content:
        xday.append(i[1])
        yvalue.append(i[2])
    data['xday'] = xday
    data['yvalue'] = yvalue
    j = json.dumps(data)
    return j