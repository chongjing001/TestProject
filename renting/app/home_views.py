import os

import uuid

from flask import Blueprint, render_template, request, jsonify, session

from app.models import House, Facility, Area, HouseImage, Order

blue_h = Blueprint('home', __name__)


@blue_h.route('/index/', methods=['GET'])
def index():
    if request.method == 'GET':
        return render_template('index.html')


@blue_h.route('/search/', methods=['GET'])
def search():
    if request.method == 'GET':
        return render_template('search.html')


@blue_h.route('/newhouse/', methods=['GET'])
def newhouse():
    if request.method == 'GET':
        return render_template('newhouse.html')


@blue_h.route('/newhouse/', methods=['POST'])
def add_newhouse():
    if request.method == 'POST':
        title = request.form.get('title')
        price = request.form.get('price')
        area = request.form.get('area_id')
        addr = request.form.get('address')
        count = request.form.get('room_count')
        acreage = request.form.get('acreage')
        unit = request.form.get('unit')
        capacity = request.form.get('capacity')
        beds = request.form.get('beds')
        deposit = request.form.get('deposit')
        min_days = request.form.get('min_days')
        max_days = request.form.get('max_days')
        facility = request.form.getlist('facility')
        house = House()
        house.title = title
        house.price = price
        house.area_id = area
        house.address = addr
        house.room_count = count
        house.acreage = acreage
        house.unit = unit
        house.capacity = capacity
        house.beds = beds
        house.deposit = deposit
        house.min_days = min_days
        house.max_days = max_days
        house.user_id = session['user_id']
        for i in facility:
            fac = Facility.query.filter_by(id=int(i)).first()
            house.facilities.append(fac)
        house.add_update()

        id = house.id
        return jsonify({'code': 200, 'msg': '请求成功', 'id': id})


@blue_h.route('/add_himg/', methods=['POST'])
def add_himg():
    if request.method == 'POST':
        house_image = request.files.get('house_image')
        id = request.form.get('house_id')
        house = House.query.get(id)

        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        STATIC_DIR = os.path.join(BASE_DIR, 'static')
        IMG_DIR = os.path.join(STATIC_DIR, 'images')

        filename = str(uuid.uuid4())
        a = house_image.mimetype.split('/')[-1:][0]
        name = filename + '.' + a

        path = os.path.join(IMG_DIR, name)
        house_image.save(path)
        house.index_image_url = '/static/images/' + name
        house.add_update()

        himg = HouseImage()
        himg.house_id = id
        himg.url = '/static/images/' + name
        himg.add_update()
        # hg = HouseImage.query.filter_by(house_id=id).all()
        # h = [i.url for i in hg]
        # count = len(h)
        return jsonify({'code': 200, 'msg': '请求成功', 'data': '/static/images/' + name})


#
@blue_h.route('/house_info/', methods=['GET'])
def house_info():
    if request.method == 'GET':
        house = House.query.filter(House.user_id == session['user_id']).all()
        h = [i.to_dict() for i in house]
        count = len(h)

        return jsonify({'code': 200, 'msg': '请求成功', 'data': h, 'count': count})


@blue_h.route('/detail/<int:id>/', methods=['GET'])
def detail(id):
    if request.method == 'GET':
        return render_template('detail.html')


# 具体房源接口
@blue_h.route('/my_detail/', methods=['GET'])
def my_detail():
    if request.method == 'GET':
        id = request.args.get('id')
        house = House.query.filter_by(id=id).first()
        flag = True  # 用于判断房源是否是自己的
        flag1 = False  # 用于判断是否登陆
        try:
            if house.user_id == int(session['user_id']):
                flag = False  # 是自己的房源
                # return jsonify({'code': 200, 'msg': '请求成功', 'data': house.to_full_dict(), 'flag': flag})
        except:
            flag1 = True  # 没有登陆

        return jsonify({'code': 200, 'msg': '请求成功', 'data': house.to_full_dict(), 'flag': flag, 'flag1': flag1})


# 房屋设施和地区接口
@blue_h.route('/fac/', methods=['GET'])
def fac():
    if request.method == 'GET':
        fa = Facility.query.all()
        area = Area.query.all()
        f = [i.to_dict() for i in fa]
        a = [i.to_dict() for i in area]
        return jsonify({'code': 200, 'msg': '请求成功', 'data': f, 'data1': a})


# 主页展示信息接口
@blue_h.route('/index_info/', methods=['GET'])
def index_info():
    if request.method == 'GET':
        house = House.query.all()
        data = []
        for i in house:
            data.append(i.to_dict())
        count = len(data)
        return jsonify({'code': 200, 'msg': '请求成功', 'data': data, 'count': count})


# 搜索接口
@blue_h.route('/s_info/', methods=['GET'])
def s_info():
    a_id = request.args.get('a_id')
    # a_name = request.args.get('a_name')
    st_date = request.args.get('st_date')
    end_date = request.args.get('end_date')

    if not all([a_id,st_date,end_date]):
        house = House.query.all()
        data = []
        for i in house:
            data.append(i.to_dict())
        count = len(data)
        return jsonify({'code': 200, 'msg': '请求成功', 'data': data, 'count': count})

    # 查询该区域的房源
    houses = House.query.filter_by(area_id=a_id)
    # 满足时间条件，查询入住时间和退房时间在首页选择时间内的房间，并排除掉这些房间
    order_list = Order.query.filter(Order.status != 'REJECTED')
    # 情况一：
    order_list1 = Order.query.filter(Order.begin_date >= st_date, Order.end_date <= end_date)
    # 情况二：
    order_list2 = order_list.filter(Order.begin_date < st_date, Order.end_date > end_date)
    # 情况三：
    order_list3 = order_list.filter(Order.end_date >= st_date, Order.end_date <= end_date)
    # 情况四：
    order_list4 = order_list.filter(Order.begin_date >= st_date, Order.begin_date <= end_date)
    # 获取订单中的房屋编号
    house_ids = [order.house_id for order in order_list2]
    for order in order_list3:
        house_ids.append(order.house_id)
    for order in order_list4:
        if order.house_id not in house_ids:
            house_ids.append(order.house_id)
    # 查询排除入住时间和离店时间在预约订单内的房屋信息
    hlist = houses.filter(House.id.notin_(house_ids))
    # 排序规则,默认根据最新排列

    hlist = [house.to_dict() for house in hlist]

    return jsonify({'code': 200, 'msg': '请求成功', 'data': hlist})
