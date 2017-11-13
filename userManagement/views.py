from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django import forms
from userManagement.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='姓名', max_length=100)
    email = forms.CharField(label="邮箱", max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


class UserLoginForm(forms.Form):
    email = forms.CharField(label="邮箱", max_length=100)
    password = forms.CharField(label='密码', widget=forms.PasswordInput())


def register(request):
    if request.method == 'POST':
        uf = UserRegisterForm(request.POST)
        if uf.is_valid():
            # 获得表单数据
            username = uf.cleaned_data['username']
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            # 添加到数据库
            User.objects.create(username=username, email=email, password=password)
            return HttpResponse('register success!!')
    else:
        uf = UserRegisterForm()
    return render(request, 'register.html', {'uf': uf})


def login(request):
    if request.method == 'POST':
        uf = UserLoginForm(request.POST)
        if uf.is_valid():
            # 获取表单用户密码
            email = uf.cleaned_data['email']
            password = uf.cleaned_data['password']
            # 获取的表单数据与数据库进行比较
            user = User.objects.filter(email__exact=email, password__exact=password)
            if user:
                # 比较成功，跳转index
                response = HttpResponseRedirect('/gao/')
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('email', email, 3600)
                return response
            else:
                # 比较失败，还在login
                return HttpResponseRedirect('/login/')
    else:
        uf = UserLoginForm()
    return render(request, 'login.html', {'uf': uf})


def index(request):
    email = request.COOKIES.get('email', '')
    return render_to_response('index.html', {'email': email})


def logout(request):
    response = HttpResponse('logout !!')
    # 清理cookie里保存username
    response.delete_cookie('email')
    return response
