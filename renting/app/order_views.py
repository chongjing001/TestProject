from flask import Blueprint, render_template, request, jsonify, session

from app.models import House, Order

blue_o = Blueprint('order', __name__)


@blue_o.route('/lorders/', methods=['GET'])
def lorders():
    if request.method == 'GET':
        return render_template('lorders.html')


@blue_o.route('/orders/', methods=['GET'])
def orders():
    if request.method == 'GET':
        return render_template('orders.html')


@blue_o.route('/order_info/', methods=['GET'])
def order_info():
    if request.method == 'GET':
        user_orders = Order.query.filter_by(user_id=session['user_id']).all()
        user_order = [i.to_dict() for i in user_orders]
        return jsonify({'code': 200, 'msg': '请求成功', 'data': user_order})


@blue_o.route('/other_info/', methods=['GET'])
def other_info():
    my_id = session['user_id']
    all_house = House.query.filter(House.user_id == my_id).all()
    hid_list = [i.id for i in all_house]
    all_orders = Order.query.filter(Order.house_id.in_(hid_list))
    cum_order = [i.to_dict() for i in all_orders]

    return jsonify({'code': 200, 'msg': '请求成功', 'data': cum_order})


@blue_o.route('/stay/', methods=['POST'])
def stay():
    if request.method == 'POST':
        order = Order()
        order.amount = request.form.get('t')[1:].split('.')[0]
        order.days = request.form.get('d')
        order.begin_date = request.form.get('st')
        order.end_date = request.form.get('et')
        order.house_price = int(order.amount) / int(order.days)
        order.user_id = session['user_id']
        order.house_id = request.form.get('h_id')

        order.add_update()

        return jsonify({'code': 200, 'msg': '请求成功'})


@blue_o.route('/booking/<int:id>/', methods=['GET'])
def booking(id):
    if request.method == 'GET':
        return render_template('booking.html')





@blue_o.route('/order/', methods=['PATCH'])
def order():
    order_id = request.form.get('order_id')
    status = request.form.get('status')
    comment = request.form.get('comment')
    order = Order.query.filter_by(id=order_id).first()
    order.status = status
    if comment:
        order.comment = comment
    order.add_update()
    return jsonify({'code': 200, 'msg': '请求成功'})
