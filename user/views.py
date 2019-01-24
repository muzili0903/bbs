# from hashlib import md5  #md5可以被彩虹表攻击
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render, redirect

# Create your views here.
from user.forms import RegisterFrom


def register(request):
    if request.method == 'POST':
        # 取出数据
        form = RegisterFrom(request.POST, request.FILES)
        if form.is_valid():
            # 创建一个user,commit参数：暂时不提交到数据库
            user = form.save(commit=False)
            # 保存图片
            # 密码加密处理
            user.password = make_password(user.password)
            # 保存用户
            user.save()
            # 登录跳转
            request.session['uid'] = user.id
            request.session['uid'] = user.nickname
            return redirect('/user/login/')
        else:
            return render(request, '', {'error': form.errors})
    return render(request, '', {})


def login(request):
    return render(request, '', {})


def logout(request):
    return render(request, '', {})


def user_info(request):
    return render(request, '', {})
