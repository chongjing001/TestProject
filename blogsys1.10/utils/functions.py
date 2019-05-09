from django.http import HttpResponseRedirect


# 装饰器

# 1. 外层函数内嵌内层函数
# 2. 外层函数返回内置函数
from django.urls import reverse


def is_login(func):
    def check_status(request):
        if request.session.get('user_id'):
            return func(request)
        else:
            return HttpResponseRedirect(reverse('user:login'))
    return check_status

