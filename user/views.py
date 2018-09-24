from django.shortcuts import redirect, render
# from comment.models import Comment   # 导入Comment评论模块
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
from django.contrib import auth  # auth模块是Django提供的标准权限管理系统,可以提供用户身份认证, 用户组和权限管理。
from django.urls import reverse    # 反向解析
from django.contrib.auth.models import User
# from comment.models import Comment
# from comment.forms import CommentForm
from .forms import *
from django.http import JsonResponse
from .models import Profile
from .tasks import send_email_by_celery
import string
import random
import time


def login_for_modal(request):
    """
    模态框
    :param request: 请求对象
    :return: json数据
    """
    login_form = LoginForm(request.POST)
    if login_form.is_valid():
        # cleaned_data是一个字典,包含了字段的信息
        # 表示清理过或者整理过的数据,比较干净的数据
        # username = login_form.cleaned_data['username']
        # password = login_form.cleaned_data['password']
        # user = auth.authenticate(username=username, password=password)
        # 判断用户是否存在
        # if user is not None:
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        # 如果没有获取到源页面就返回到首页
        data = {'status': 'SUCCESS'}
    else:
        data = {'status': 'ERROR'}
    return JsonResponse(data)


def login(request):
    """
    用户登录逻辑处理
    :param request:
    :return: 登录视图
    """
    '''
    # 利用request的POST方法获取form表单中的post数据
    username = request.POST.get('username')
    password = request.POST.get('password')
    # 通过用户名和密码构造用户连接
    user = auth.authenticate(username=username, password=password)
    # 获取源页面
    # 如果获取不到源页面,就使用反向解析到首页
    referer = request.META.get('HTTP_REFERER', reverse('blog:home'))

    # 判断用户是否存在
    if user is not None:
        auth.login(request, user)
        # 如果没有获取到源页面就返回到首页
        return redirect(referer)
    else:
        context = {'message': '用户名或密码错误'}
        return render(request, 'blog/error.html', context)
    '''
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        # 判断是否有效
        # 验证通过
        if login_form.is_valid():
            # cleaned_data是一个字典,包含了字段的信息
            # 表示清理过或者整理过的数据,比较干净的数据
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = auth.authenticate(username=username, password=password)
            # 判断用户是否存在
            # if user is not None:
            user = login_form.cleaned_data['user']
            auth.login(request, user)
            # 如果没有获取到源页面就返回到首页
            referer = request.GET.get('from', reverse('blog:blog'))
            return redirect(referer)

    # 验证失败
    else:
        # login_form对象会自动创建表单
        login_form = LoginForm()

    context = {'login_form': login_form}
    return render(request, 'user/login.html', context)


def register(request):
    """
    用户注册功能相关处理
    :param request: 请求对象
    :return: 注册成功返回首页，失败返回注册表单
    """
    if request.method == 'POST':
        reg_form = RegForm(request.POST, request=request)
        # 判断是否有效
        # 验证通过
        if reg_form.is_valid():
            # 第一种注册方法
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            # 清楚session
            del request.sesssion['register_code']
            # 登录用户
            user = auth.authenticate(username=username, password=password)
            auth.login(request, user)
            return redirect(request.GET.get('from', reverse('blog:home')))

        '''
            # 第二种注册方法
            user = User()
            user.username = username
            user.email = email
            user.set_password(password)
            user.save()
    
        '''

    # 验证失败
    else:
        # login_form对象会自动创建表单
        reg_form = RegForm()

    context = {'reg_form': reg_form}
    return render(request, 'user/register.html', context)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('blog:home')))


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def about(request):
    context = {}
    return render(request, 'user/about.html',   context)


def change_name(request):
    """修改昵称"""
    if request.method == 'POST':
        name_form = ChangeNameForm(request.POST, user=request.user)
        if name_form.is_valid():
            new_nickname = name_form.cleaned_data['new_nickname']
            profile, created = Profile.objects.get_or_create(user=request.user)
            profile.nickname = new_nickname
            profile.save()
            return redirect(request.GET.get('from', reverse('blog:home')))

    else:
        name_form = ChangeNameForm()

    context = {'name_form': name_form}
    return render(request, 'user/change_name.html', context)


def change_password(request):
    """修改密码"""
    if request.method == 'POST':
        password_form = ChangePasswordForm(request.POST, user=request.user)
        if password_form.is_valid():
            user = request.user
            new_password = password_form.cleaned_data['new_password']
            # past_password = password_form.cleaned_data['past_password']

            # 直接赋值是没办法加密的
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect('user:login')

    else:
        password_form = ChangePasswordForm()

    context = {'password_form': password_form}
    return render(request, 'user/change_password.html', context)


def forgot_password(request):
    """忘记密码"""
    if request.method == 'POST':
        forgot_form = ForgotPasswordForm(request.POST, request=request)
        if forgot_form.is_valid():
            new_password = forgot_form.cleaned_data['new_password']
            email = forgot_form.cleaned_data['email']
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()

            # 情书session
            del request.session['forgot_password_code']
            return redirect('user:login')

    else:
        forgot_form = ForgotPasswordForm()

    context = {'forgot_form': forgot_form}
    return render(request, 'user/forgot_password.html', context)


def bind_email(request):
    """绑定邮箱"""
    if request.method == 'POST':
        email_form = BindEmailForm(request.POST, request=request)
        if email_form.is_valid():
            email = email_form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清楚session
            del request.sesssion['bind_eamil_code']
            return redirect(request.GET.get('from', reverse('blog:home')))

    else:
        email_form = BindEmailForm()

    context = {'email_form': email_form}
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email', '')
    send_for = request.GET.get('send_for', '')
    data = {}
    if email != '':
        # 生成验证码
        # 利用random的sample方法
        # 参数：string.ascii_letters，返回所有大小写字母
        # 参数：string.digits,返回0-9的数字
        # 返回的结果是一个列表
        code = ''.join(random.sample(string.ascii_letters + string.digits, 4))
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 30:
            data["status"] = 'ERROR'
        else:
            # session默认有效期是两星期
            request.session[send_for] = code
            request.session['send_code_time'] = now

            # 发送邮件
            send_email_by_celery.delay(code, email)

            data["status"] = 'SUCCESS'
    else:
        data["status"] = 'ERROR'
    return JsonResponse(data)
