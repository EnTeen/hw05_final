from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm, CommentForm
from .models import Group, Post, User
from .utilites import get_page


def index(request):
    posts = Post.objects.all()
    page_obj = get_page(request, posts)
    return render(
        request, 'posts/index.html', {'page_obj': page_obj},
    )


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()
    page_obj = get_page(request, posts)
    return render(
        request, 'posts/group_list.html',
        {'group': group, 'page_obj': page_obj},
    )


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    page_obj = get_page(request, posts)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    author = get_object_or_404(User, username=post.author)
    comments = post.comments.all()
    form = CommentForm()
    context = {
        'post': post,
        'author': author,
        'comments': comments,
        'form': form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None,)
    if not form.is_valid():
        return render(
            request, 'posts/create_and_edit_post.html',
            {'form': form, 'username': request.user}
        )
    post = form.save(commit=False)
    post.author = request.user
    post.save()
    return redirect('posts:profile', username=post.author)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return render('posts:profile', username=request.user)
    form = PostForm(request.POST or None, files=request.FILES or None, instance=post)
    if not form.is_valid():
        return render(
            request, 'posts/create_and_edit_post.html',
            {'form': form, 'post': post, 'is_edit': True},
        )
    post.author = request.user
    post = form.save()
    return redirect('posts:post_detail', post_id=post_id, )

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)