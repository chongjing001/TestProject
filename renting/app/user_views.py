import os
import random
import re
import uuid

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session

from flask_login import login_user, login_required, logout_user, LoginManager

from utils.functions import is_login
from app.models import User

login_manage = LoginManager()

blue = Blueprint('user', __name__)


# @blue.before_request
# def before():
#     user_id = session.get('user_id')
#     if user_id:
#         user = User.query.filter_by(id=user_id).first()
#         request.user = user
#
#
#     if not user_id:
#         return redirect(url_for('home.index'))

@blue.route('/index/', methods=['GET', 'POST'])
@is_login
# @login_required
def index():
    if request.method == 'GET':
        return render_template('my.html')


@blue.route('/login/', methods=['GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')


@blue.route('/user_info/', methods=['GET'])
def user_info():
    try:
        user_id = session['user_id']
        user = User.query.get(user_id)
        flag = False
        return jsonify(
            {'code': 200, 'msg': '请求成功', 'data': user.to_basic_dict(), 'data1': user.to_auth_dict(), 'flag': flag})
    except:
        flag = True
        return jsonify(
        {'code': 200, 'msg': '请求成功', 'flag': flag})


@blue.route('/login/', methods=['POST'])
def my_login():
    if request.method == 'POST':
        phone = request.form.get('mobile')
        password = request.form.get('passwd')
        user = User.query.filter(User.phone == phone).first()
        if not all([phone, password]):
            return jsonify({'code': 1003, 'msg': '请填写完整信息'})
        if user:
            if user.check_pwd(password):
                login_user(user)
                return jsonify({'code': 200, 'msg': '请求成功'})
            else:
                return jsonify({'code': 1001, 'msg': '密码错误'})
        else:
            return jsonify({'code': 1002, 'msg': '该手机号没有注册！！！'})


@blue.route('/register/', methods=['GET'])
def register():
    if request.method == 'GET':
        return render_template('register.html')


@blue.route('/register/', methods=['POST'])
def my_register():
    # 获取参数
    mobile = request.form.get('mobile')
    imagecode = request.form.get('imageCode')
    passwd = request.form.get('passwd')
    passwd2 = request.form.get('passwd2')
    # 1.验证参数是否都填写了
    if not all([mobile, imagecode, passwd, passwd2]):
        return jsonify({'code': 1001, 'msg': '请填写完整信息'})

    # 2.验证手机号是否正确
    if not re.match('^1[3456789]\d{9}$', mobile):
        return jsonify({'code': 1002, 'msg': '手机号错误'})
    # 3.验证图片验证码
    if session['imageCode'] != imagecode:
        return jsonify({'code': 1003, 'msg': '验证码错误'})
    # 4.密码和确认密码是否一致
    if passwd != passwd2:
        return jsonify({'code': 1004, 'msg': '密码不一致'})

    # 验证手机号是否被注册
    user = User.query.filter_by(phone=mobile).first()
    if user:
        return jsonify({'code': 1005, 'msg': '手机号已被注册'})
    # 创建注册信息
    user = User()
    user.phone = mobile
    user.password = passwd
    user.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})


# 验证码
@blue.route('/code/')
def get_code():
    # 获取验证码
    # 1.
    # 2.后端只生成随机参数，返回给页面，在页面中生成图片（前端）
    s = '1234567890qwertyuiopasdfghjklmnbvcxz'
    code = ''
    for _ in range(4):
        code += random.choice(s)
    session['imageCode'] = code
    return jsonify({'code': 200, 'msg': '请求成功', 'data': code})


@blue.route('/logout/', methods=['GET'])
def logout():
    if request.method == 'GET':
        del session['user_id']
    return redirect(url_for('home.index'))


@blue.route('/house/', methods=['GET', 'POST'])
def house():
    if request.method == 'GET':
        return render_template('myhouse.html')


@blue.route('/auth/', methods=['GET'])
def auth():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        return render_template('auth.html', user=user)


@blue.route('/my_auth/', methods=['GET'])
def my_auth():
    if request.method == 'GET':
        id_name = request.args.get('id_name')
        id_card = request.args.get('id_card')
        if not all([id_name, id_card]):
            return jsonify({'code': 1001, 'msg': '请填写完整信息'})

        if not re.match('([\u4e00-\u9fa5]){2,7}', id_name):
            return jsonify({'code': 1003, 'msg': '请填写合法姓名'})

        all_id_card = User.query.all()
        id_card_list = [i.id_card for i in all_id_card]
        if id_card in id_card_list:
            return jsonify({'code': 1004, 'msg': '该证件号已注册'})

        # if not re.match('^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$', id_card):
        if len(id_card) < 10:
            return jsonify({'code': 1002, 'msg': '请填写合法的身份证号'})
        user = User.query.get(session['user_id'])
        user.id_name = id_name
        user.id_card = id_card
        user.add_update()
        return jsonify({'code': 200, 'msg': '请求成功'})


@blue.route('/profile/', methods=['GET'])
def profile():
    if request.method == 'GET':
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user)


@blue.route('/profile/', methods=['POST'])
def my_profile():
    if request.method == 'POST':
        avatar = request.files.get('avatar')
        username = request.form.get('name')
        user = User.query.get(session['user_id'])
        if avatar:
            BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            STATIC_DIR = os.path.join(BASE_DIR, 'static')
            MEDIA_DIR = os.path.join(STATIC_DIR, 'media')
            filename = str(uuid.uuid4())
            a = avatar.mimetype.split('/')[-1:][0]
            name = filename + '.' + a

            path = os.path.join(MEDIA_DIR, name)

            avatar.save(path)

            user.avatar = name
            user.add_update()
            return jsonify({'code': 200, 'msg': '请求成功'})

        if username:
            user.name = username
            user.add_update()

            return jsonify({'code': 200, 'msg': '请求成功'})


@login_manage.user_loader
def load_user(user_id):
    # 定义被login_manage装饰的回调函数
    # 返回的是当前登陆系统的用户对象
    return User.query.filter(User.id == user_id).first()
