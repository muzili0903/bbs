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
            return render(request, '', {'error': form.errors})
    return render(request, '', {})


def login(request):
    return render(request, '', {})


def logout(request):
    # 清理当前的session信息
    request.session.flush()
    return redirect('/user/login')


def user_info(request):
    uid = request.session.get('uid')
    user = User.objects.get(pk=uid)
    return render(request, '', {'user': user})
