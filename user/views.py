# from hashlib import md5  #md5可以被彩虹表攻击
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

# Create your views here.
from user.forms import RegisterFrom
from user.models import User


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
            request.session['avatar'] = user.icon.url
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
            return render(request, 'login.html', {'error': '用户名或密码错误'})
        if check_password(password, user.password):
            # 登录跳转
            request.session['uid'] = user.id
            request.session['nickname'] = user.nickname
            request.session['avatar'] = user.icon.url
            return redirect('/user/info/')
        else:
            return render(request, 'login.html', {'error': '用户名或密码错误'})
    return render(request, 'login.html')


def logout(request):
    # 清理当前的session信息
    request.session.flush()
    return redirect('/user/login')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(request, 'user_info.html', {'user': user})
