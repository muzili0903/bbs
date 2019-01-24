from math import ceil

from django.shortcuts import render, redirect

# Create your views here.
from post.models import Post


def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        post = Post.objects.create(title=title, content=content)
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        return render(request, '', {})


def edit_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(pk=post_id)
        post.title = request.POST.get('title')
        post.content = request.POST.get('content')
        post.save()
        return redirect('/post/read/?post_id=%s' % post.id)
    else:
        post_id = request.GET.get('post_id')
        post = Post.objects.get(pk=post_id)
        return render(request, '', {'post': post})


def read_post(request):
    post_id = request.GET.get('post_id')
    post = Post.objects.get(pk=post_id)
    return render(request, '', {'post': post})


def delete_post(request):
    post_id = request.GET.get('post_id')
    Post.objects.get(pk=post_id).delete()
    return redirect('/')


def list_post(request):
    page = int(request.GET.get('page', 1))  # 当前页码，默认为1
    total = Post.objects.count()  # 总文章
    per_page = 10  # 每页页数
    pages = int(ceil(total / per_page))  # 总页数

    start = (page - 1) * per_page
    end = start + per_page
    # 执行all的时候不会把所有的对象取出来，all是赖加载,如果all后面没有条件，就会把所有的对象加载起来
    posts = Post.objects.all().order_by('-id')[start:end]
    # select * from post where offset start limit per_page
    return render(request, '', {'posts': posts, 'pages': range(pages)})


def search_post(request):
    keyword = request.POST.get('keyword')
    posts = Post.objects.filter(content__contains=keyword)
    return render(request, '', {'posts': posts})
