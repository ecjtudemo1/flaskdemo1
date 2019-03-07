
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    """管理员登录表单"""
    account = StringField('账号：', validators=[DataRequired("请输入账号！")], description="账号")
                          #render_kw={"type": "text",  "class": "text" ,
                                    #"value": "Username","onfocus":"this.value = '';",
                                     #"onblur": "if (this.value == '') {this.value = 'Username';}"}#账号
    pwd = PasswordField('密码：', validators=[DataRequired("请输入密码！")], description="密码")
                        #render_kw={
                            #"type" : "password",
    #"value" : "Password",
    #"onfocus" : "this.value = '';",
    #"onblur" : "if (this.value == '') {this.value = 'Password';}"

                       # })#required变为datarequired
    remember_me = BooleanField('记住我')#记住管理员账号
    submit = SubmitField('登录') #提交按钮
