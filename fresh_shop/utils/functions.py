import random
import time

from django.http import HttpResponseRedirect
from django.urls import reverse


def is_login(func):
    def check(request):
        try:
            # 获取session中已保存的user_id值
            request.session['user_id']
        except:
            # 调转到登录
            return HttpResponseRedirect(reverse('user:login'))
        return func(request)

    return check


def get_order_sn():
    # 获取订单号
    s = '1234567890qwertyuiopasdfghjklzxcvbnmLPOKMIJNUHBYGVTFCRDXESZWAQ'
    order_sn = ''
    for _ in range(20):
        order_sn += random.choice(s)
    order_sn += str(time.time())
    print(order_sn)
    return order_sn
