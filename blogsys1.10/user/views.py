from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.
from user.models import User
from utils.functions import is_login



def login(request):

    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = User.objects.filter(username=username).first()
            if check_password(password, user.password):
                request.session['user_id'] = user.id
                return HttpResponseRedirect(reverse('article:index'))
            else:
                msg = '密码错误'
                return render(request, 'login.html',{'msg':msg})
        except:
            msg = '账号不存在'
            return render(request, 'login.html', {'msg': msg})


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if User.objects.filter(username=username):
            msg = '账号已存在'
            return render(request, 'register.html', {'msg': msg})
        if password != password2:
            msg = '密码不一致'
            return render(request, 'register.html', {'msg': msg})
        password = make_password(password)
        User.objects.create(username=username, password=password)

        return HttpResponseRedirect(reverse('user:login'))
