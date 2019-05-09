from django.core.paginator import Paginator
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from cart.models import ShoppingCart
from fresh_shop.settings import ORDER_NUMBER
from goods.models import Goods
from order.models import OrderInfo, OrderGoods
from user.forms import AddressForm
from user.models import UserAddress
from django.http import HttpResponseRedirect, JsonResponse

from utils.functions import get_order_sn


def user_center(request):
    if request.method == 'GET':
        activate = 'info'
        user_id = request.session.get('user_id')
        addr_user = UserAddress.objects.filter(user_id=user_id).first()
        all_goods = Goods.objects.all()
        goods_id = []
        se_goods = request.session.get('goods')
        for goods in se_goods:
            goods_id.append(goods[0])
        goods_list = []
        for goods in all_goods:
            if goods.id in goods_id:
                goods_list.append(goods)

        return render(request, 'user_center_info.html', {'activate': activate, 'addr_user': addr_user,'goods_list':goods_list})


def user_center_order(request):
    if request.method == 'GET':
        # 获取登陆系统的id值
        page = request.GET.get('page', 1)
        user_id = request.session.get('user_id')
        # 查询当前用户的订单信息
        orders = OrderInfo.objects.filter(user_id=user_id)
        status = OrderInfo.ORDER_STATUS
        # 分页
        pg = Paginator(orders, ORDER_NUMBER)
        orders = pg.page(page)
        activate = 'order'
        return render(request, 'user_center_order.html', {'orders': orders, 'status': status, 'activate': activate})


def user_center_site(request):
    if request.method == 'GET':
        user_id = request.session.get('user_id')
        user_address = UserAddress.objects.filter(user_id=user_id)
        activate = 'site'
        return render(request, 'user_center_site.html', {'user_address': user_address, 'activate': activate})
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            address = form.cleaned_data['address']
            postcode = form.cleaned_data['postcode']
            mobile = form.cleaned_data['mobile']
            user_id = request.session.get('user_id')
            UserAddress.objects.create(user_id=user_id,
                                       address=address,
                                       signer_name=username,
                                       signer_mobile=mobile,
                                       signer_postcode=postcode)
            return HttpResponseRedirect(reverse('order:user_center_site'))
        else:
            errors = form.errors
            return render(request, 'user_center_site.html', {'errors': errors})


def place_order(request):
    if request.method == 'GET':
        # 获取当前登录系统的用户
        user = request.user
        carts = ShoppingCart.objects.filter(user=user, is_select=True).all()
        count = len(carts)
        if not count:
            msg = '当前没有任何商品，不能结算'
            return render(request, 'cart.html', {'msg': msg})
        # 计算小计和总价
        total_price = 0
        for cart in carts:
            # 小计金额
            price = cart.goods.shop_price * cart.nums
            cart.goods_price = price
            # 总金额
            total_price += price
        #
        user_address = UserAddress.objects.filter(user=user).all()

        return render(request, 'place_order.html',
                      {'carts': carts, 'total_price': total_price, 'count': count, 'user_address': user_address})


def order(request):
    if request.method == 'POST':
        ad_id = request.POST.get('ad_id')

        user_id = request.session.get('user_id')
        order_sn = get_order_sn()
        shop_cart = ShoppingCart.objects.filter(user_id=user_id,
                                                is_select=True)
        order_mount = 0
        for cart in shop_cart:
            order_mount += cart.goods.shop_price * cart.nums

        # 收货信息
        user_address = UserAddress.objects.filter(pk=ad_id).first()

        order = OrderInfo.objects.create(user_id=user_id,
                                         order_sn=order_sn,
                                         order_mount=order_mount,
                                         address=user_address.address,
                                         signer_name=user_address.signer_name,
                                         signer_mobile=user_address.signer_mobile
                                         )
        # 创建订单详情
        for cart in shop_cart:
            OrderGoods.objects.create(order=order,
                                      goods=cart.goods,
                                      goods_nums=cart.nums)
        # 删除购物车
        shop_cart.delete()
        session_goods = request.session.get('goods')
        for se_goods in session_goods[:]:
            # se_goods结构[goods_id,num,is_select]
            if se_goods[2]:
                session_goods.remove(se_goods)
        request.session['goods'] = session_goods
        return JsonResponse({'code': 200, 'msg': '请求成功'})
