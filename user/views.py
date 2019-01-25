# from hashlib import md5  #md5可以被彩虹表攻击
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect
from django.conf import settings

from user.forms import RegisterFrom
from user.models import User
from user.helper import get_access_token, get_user_show


def register(request):
    if request.method == 'POST':
        # 取出数据
        form = RegisterFrom(request.POST, request.FILES)
        if form.is_valid():
            # 创建一个user,commit参数：暂时不提交到数据库
            user = form.save(commit=False)
            # TODO保存图片
            # 密码加密处理
            user.password = make_password(user.password)
            # 保存用户
            user.save()
            # 登录跳转
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'register.html', {'error': form.errors})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        nickname = request.POST.get('nickname')
        password = request.POST.get('password')
        try:
            user = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': '用户名或密码错误', 'auth_url': settings.WB_AUTH_URL})
        if check_password(password, user.password):
            # 登录跳转
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.avatar
            return redirect('/user/info/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误', 'auth_url': settings.WB_AUTH_URL})
    return render(request, 'login.html', {'auth_url': settings.WB_AUTH_URL})


def logout(request):
    # 清理当前的session信息
    request.session.flush()
    return redirect('/user/login')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(request, 'user_info.html', {'user': user})


def wb_callback(request):
    code = request.GET.get('code')
    # 获取access token
    result = get_access_token(code)
    if 'error' in result:
        return render(request, 'login.html', {'error': '用户名或密码错误', 'auth_url': settings.WB_AUTH_URL})
    access_token = result['access_token']
    uid = result['uid']

    # 获取用户信息
    result = get_user_show(access_token, uid)
    if 'error' in result:
        return render(request, 'login.html', {'error': '用户名或密码错误', 'auth_url': settings.WB_AUTH_URL})
    screen_name = result['screen_name']
    avatar_url = result['avatar_hd']
    # 注册、登录  如果是创建出来的，created为TRUE，否则为false
    user, created = User.objects.get_or_create(nickname=screen_name)
    if created:
        user.plt_icon = avatar_url
        user.save()
    # 登录跳转
    request.session['uid'] = user.id
    request.session['nickname'] = user.nickname
    request.session['avatar'] = user.avatar
    return redirect('/user/info/')
