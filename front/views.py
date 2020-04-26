from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .forms import LoginForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


# 人为验证是否存在username，此useranme非真正useranme, 为标识id
def my_authenticate(telephone, password):
    print(telephone)
    print(password)
    user = User.objects.filter(extension__telephone=telephone).first()
    print(user)
    if user:
        is_correct = user.check_password(password)
        if is_correct:
            return user
        else:
            return None
    else:
        return None


def create_user(request):
    username = 'joe'
    password = '123456789'
    telephone = '1815424j912'
    user = User.objects.create_user(username=username, password=password)
    user.extension.telephone = telephone
    user.save()
    return HttpResponse('成功创建用户')


def my_login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            telephone = form.cleaned_data.get('telephone')
            remember = form.cleaned_data.get('remember')
            password = form.cleaned_data.get('password')
            user = my_authenticate(telephone=telephone, password=password)
            if user:
                login(request, user)
                if remember == 1:
                    request.session.set_expiry(None)
                else:
                    request.session.set_expiry(0)
            else:
                return HttpResponse('用户名或密码错误')
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            else:
                return HttpResponse('登录成功')
        else:
            print(form.errors)
            return redirect(reversed('login'))


def my_logout(request):
    user_id = request.session.get('_auth_user_id')
    username = User.objects.get(pk=user_id).username
    logout(request)
    return HttpResponse('用户%s退出登录' % username)


#测试跳转的页面，如果用户没有登录，跳转到登录页面
@login_required(login_url='/login/')
def profile(request):
    user_id = request.session.get('_auth_user_id')
    username = User.objects.get(pk=user_id).username
    return HttpResponse('个人主页，您是用户：%s' % username)