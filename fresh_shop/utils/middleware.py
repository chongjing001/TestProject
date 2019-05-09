import logging
import re
import time

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin

from cart.models import ShoppingCart
from user.models import User

# 获取logger
logger = logging.getLogger(__name__)


class LogMiddleware(MiddlewareMixin):

    def process_request(self, request):
        # url到服务器的时候，经过中间件最先执行的方法
        request.init_time = time.time()
        request.init_body = request.body

    def process_response(self, request, response):
        try:
            # 经过中间件，最后执行的方法
            # 计算请求到响应的时间
            count_time = time.time() - request.init_time
            # 获取响应的状态码
            code = response.status_code
            # 获取请求的内容
            req_body = request.init_body
            # 获取想要的内容
            res_body = response.content

            msg = '%s %s %s %s' % (count_time, code, req_body, res_body)
            # 写入日志信息
            logger.info(msg)
        except Exception as e:
            logger.critical('log error, Exception:%s' % e)

        return response


class UserMiddleware(MiddlewareMixin):

    def process_request(self, request):

        # 获取登录时, 向request.session中保存的user_id值
        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
        # 登陆校验,区分需要登陆校验的地址
        # 如果请求的path为去结算的路由
        path = request.path
        if path == '/':
            return None
        # 不需要做登陆校验的地址
        not_need_check = ['/media/.*/', '/static/.*/', '/user/register/', '/user/login/', '/goods/index/',
                          '/goods/detail/.*/', '/cart/.*/']
        for check_path in not_need_check:
            if re.match(check_path, path):
                # 当前path路径为不需要做登陆校验的路由
                return None
        # path为需要做登陆校验的路由时，判断用户是否登陆，没有登录则跳转到登陆
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))


class SessionToDbMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # 同步session和数据库中的商品信息
        # 判断用户是否登陆，登陆才能数据同步
        user_id = request.session.get('user_id')
        if user_id:
            # 同步
            # 判断session中的商品是否存在数据库中，如果存在则更新

            # 否则创建

            # 同步数据库的数据到session中
            session_goods = request.session.get('goods')
            if session_goods:
                for se_goods in session_goods:
                    cart = ShoppingCart.objects.filter(user_id=user_id, goods_id=se_goods[0]).first()
                    # 更新商品信息
                    if cart:
                        if cart.nums != se_goods[1] or cart.is_select != se_goods[2]:
                            cart.nums = se_goods[1]
                            cart.is_select = se_goods[2]
                            cart.save()
                    else:
                        # 创建
                        ShoppingCart.objects.create(user_id=user_id,
                                                    goods_id=se_goods[0],
                                                    nums=se_goods[1],
                                                    is_select=se_goods[2])

            # 同步数据库中的数据到session中
            db_carts = ShoppingCart.objects.filter(user_id=user_id)
            if db_carts:
                # 写法一
                new_session_goods = [[cart.goods_id, cart.nums, cart.is_select] for cart in db_carts]
                request.session['goods'] = new_session_goods
                # 写法二
                # result = []
                # for cart in db_carts:
                #     data = [cart.goods_id, cart.nums, cart.is_select]
                #     result.append(data)
        return response
