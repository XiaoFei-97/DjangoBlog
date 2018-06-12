from django.shortcuts import redirect, render
# from comment.models import Comment   # 导入Comment评论模块
# contenttypes 是Django内置的一个应用，可以追踪项目中所有app和model的对应关系，并记录在ContentType表中
from django.contrib import auth  # auth模块是Django提供的标准权限管理系统,可以提供用户身份认证, 用户组和权限管理。
from django.urls import reverse    # 反向解析
from user.forms import RegForm
from django.contrib.auth.models import User
# from comment.models import Comment
# from comment.forms import CommentForm
from user.forms import LoginForm
from django.http import JsonResponse


def login_for_modal(request):
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
    """用户登录逻辑处理"""
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
    """用户注册功能相关处理"""
    if request.method == 'POST':
        reg_form = RegForm(request.POST)
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
    return render(request, 'user/about.html',context)