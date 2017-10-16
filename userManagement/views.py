from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django import forms
from userManagement.models import User


class UserRegisterForm(forms.Form):
    username = forms.CharField(label='姓名',
                               max_length=100,
                               error_messages={'required': "姓名不能为空"})
    email = forms.EmailField(label="邮箱",
                             max_length=100,
                             error_messages={'required': "邮箱不能为空",
                                             'invalid': "邮箱格式错误"})
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(),
                               max_length=20,
                               min_length=6,
                               error_messages={'required': "密码不能为空"})
    password2 = forms.CharField(label='确认密码',
                                widget=forms.PasswordInput(),
                                max_length=20,
                                min_length=6,
                                error_messages={'required': "密码不能为空"})

    def clean_password2(self):
        password_1 = self.cleaned_data['password']
        password_2 = self.cleaned_data['password2']
        if password_1 and password_2 and password_1 != password_2:
            raise forms.ValidationError('密码验证失败', code='invalid')
        return password_2

    def clean_email(self):
        try:
            email = self.cleaned_data['email']
        except:
            raise forms.ValidationError("邮箱输入错误")
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError("该邮箱已存在")
        return email


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="邮箱",
                             max_length=100,
                             error_messages={'required': "邮箱不能为空",
                                             'invalid': "邮箱格式错误"})
    password = forms.CharField(label='密码',
                               widget=forms.PasswordInput(),
                               max_length=20,
                               min_length=6,
                               error_messages={'required': "密码不能为空"})


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
    print(uf)
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
                response = HttpResponseRedirect('/index/')
                # 将username写入浏览器cookie,失效时间为3600
                response.set_cookie('username', email, 3600)
                return response
            else:
                # 比较失败，还在login
                return HttpResponseRedirect('/login/?login_fail=1')
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
