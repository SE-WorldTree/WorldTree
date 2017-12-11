import json

#import simplejson as simplejson
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from users.models import User, EmailVerifyRecord
from users.utils import send_register_email
from .forms import RegisterForm
import base64


def register(request):
    # 只有当请求为 POST 时，才表示用户提交了注册信息
    if request.method == 'POST':
        # request.POST 是一个类字典数据结构，记录了用户提交的注册信息
        # 这里提交的就是用户名（username）、密码（password）、邮箱（email）
        # 用这些数据实例化一个用户注册表单
        form = RegisterForm(request.POST)

        # 验证数据的合法性
        if form.is_valid():
            # 如果提交数据合法，调用表单的 save 方法将用户数据保存到数据库
            #form.save()
            cd = form.cleaned_data
            #new_user = form.save()
            username, password, email = cd['username'], cd['password1'], cd['email']
            user = User.objects.create(username=username, password=password, email=email, is_active=False)
            user.set_password(password)
            send_register_email(email, send_type="register")
            user.save()
            # 注册成功，跳转回首页
            return redirect('/')
    else:
        # 请求不是 POST，表明用户正在访问注册页面，展示一个空的注册表单给用户
        form = RegisterForm()

    # 渲染模板
    # 如果用户正在访问注册页面，则渲染的是一个空的注册表单
    # 如果用户通过表单提交注册信息，但是数据验证不合法，则渲染的是一个带有错误信息的表单
    return render(request, 'users/register.html', context={'form': form})


class ActiveUserView(View):
    def get(self, request, active_code):
        # 用code在数据库中过滤处信息
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        print(active_code)
        if all_records:
            for record in all_records:
                email = record.email
                print(email)
                # 通过邮箱查找到对应的用户
                user = User.objects.get(email=email)
                # 激活用户
                user.is_active = True
                user.save()
        else:
            return render(request, "registration/active_fail.html")
        return HttpResponseRedirect(reverse('login'))


def index(request):
    return render(request, 'index.html')


def rejson(request):
    proposals = [{'short_name': 'a1'}, {'short_name': 'a2'}, {'short_name': 'b1'}, {'short_name': 'b2'}]
    proposals = json.dumps(proposals)
    return HttpResponse(proposals)
