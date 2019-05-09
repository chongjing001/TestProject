from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.
from django.urls import reverse

from user.forms import RegisterForm, LoginForm
from user.models import User


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        # 使用表单form校验
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 账号不存在数据库，密码一致，邮箱格式正确
            username = form.cleaned_data['username']
            password = make_password(form.cleaned_data['pwd'])
            email = form.cleaned_data['email']
            User.objects.create(username=username,
                                password=password,
                                email=email)
            return HttpResponseRedirect(reverse('user:login'))
        else:
            # 获取表单验证不通过
            errors = form.errors
            return render(request, 'register.html', {'errors': errors})


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # 用户名存在，密码相同
            username = form.cleaned_data['username']
            user = User.objects.filter(username=username).first()
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('goods:index'))
        else:
            erorrs = form.errors
            return render(request, 'login.html', {'erorrs': erorrs})


def logout(request):
    if request.method == 'GET':
        # 删掉session中的键值对user_id
        del request.session['user_id']
        # 删除商品信息
        if request.session.get('goods'):
            del request.session['goods']
        return HttpResponseRedirect(reverse('goods:index'))
