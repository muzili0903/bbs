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
    return render(request, '', {})


def list_post(request):
    return render(request, '', {})


def search_post(request):
    return render(request, '', {})
