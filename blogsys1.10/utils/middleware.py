import re
import time
import logging

from django.shortcuts import render
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseRedirect

from user.models import User

# 获取处理日志的logger
logger = logging.getLogger(__name__)


class TestMiddleware1(MiddlewareMixin):
    def process_request(self, request):
        print('test1 process request')
        # 地所有的请求都进行登陆状态的校验
        path = request.path
        if path in ['/user/register/', '/user/login/']:
            # 跳过以下所有代码，直接访问路由对应的视图函数
            return None
        try:
            user_id = request.session['user_id']
            print('1233333333')
            print(user_id)
            user = User.objects.get(pk=user_id)
            request.user = user
            return None
        except Exception as e:
            print('================================================')
            return HttpResponseRedirect(reverse('user:login'))

    def process_view(self, request, view_func, view_args, view_kwargs):
        print('test1 view')

    def process_response(self, request, response):
        print('test1 process response')
        return response


class UserMiddleware(MiddlewareMixin):
    def process_request(selfself, request):

        user_id = request.session.get('user_id')
        if user_id:
            user = User.objects.filter(pk=user_id).first()
            request.user = user
            return None
        path = request.path
        if path == '/':
            return None
        not_need_path = ['/user/login/', '/user/register/']
        for check_path in not_need_path:
            if re.match(check_path, path):
                return None
        if not user_id:
            return HttpResponseRedirect(reverse('user:login'))

    def process_exception(self, request, exception):
        msg = '该账号不存在'
        return render(request, 'login.html', {'msg': msg})

    def process_response(self, request, response):
        return response


# class TestMiddleware2(MiddlewareMixin):
#     def process_request(self, request):
#         print('test2 process request')
#
#     def process_view(self, request, view_func, view_args, view_kwargs):
#         print('test2 view')
#
#     def process_response(self, request, response):
#         print('test2 process response')
#         return response


class LoggingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.init_time = time.time()

    def process_response(self, request, response):
        try:
            # 请求到响应之间消耗时长
            count_times = time.time() - request.init_time
            # 请求地址和请求方式
            path = request.path
            method = request.method
            # 响应的状态码和内容
            status = request.status_code
            content = response.content
            # 日志记录的信息
            message = '%s %s %s %s %s ' % (path, method, status, content, count_times)
            logger.info(message)
        except Exception as e:
            logger.critical('log error: %s ' % e)
        return response
