import math
from functools import reduce

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites import requests
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from blog.forms import PostCreateForm, PostUpdateForm, CommentForm
from blog.models import Category, Post, Rating


def main_page(request):
    categories = Category.objects.all()
    context = {
        'categories': categories,
    }
    return render(request, 'blog/index.html', context)


@login_required()
def user_posts(request):
    posts = Post.objects.filter(author=request.user)
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj
    }
    return render(request, 'blog/user_posts.html', context)


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostCreateForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
    form = PostCreateForm()
    return render(request, 'blog/post_create.html',
                  context={'form': form})


def category_posts(request, pk):
    category = Category.objects.filter(id=pk).first()
    posts = Post.objects.filter(category=category, published=True)
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'blog/category_posts.html',
                  context={'category': category, 'posts': page_obj})


def search(request):
    query = request.GET.get('q')
    posts = Post.objects.filter(title__icontains=query, published=True)
    return render(request, 'blog/search.html',
                  context={'posts': posts})


def post_detail(request, pk):
    owner = None
    post = Post.objects.filter(id=pk).first()
    prev_post = Post.objects.filter(id=pk-1).first()
    next_post = Post.objects.filter(id=pk+1).first()

    not_anonymous = not (isinstance(request.user, AnonymousUser))
    if not_anonymous and request.user == post.author:
        pass
    else:
        post.seen_amount += 1
        post.save()

    if request.user == post.author:
        owner = True

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()

    form = CommentForm()
    context = {
        'post': post,
        'owner': owner,
        'form': form,
        'prev_post': prev_post,
        'next_post': next_post
    }
    return render(request, 'blog/post_detail.html',
                  context)


def post_update(request, pk):
    post = Post.objects.filter(id=pk).first()
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('my_posts')
    form = PostUpdateForm(instance=post)
    context = {
        'post': post,
        'form': form
    }
    return render(request, 'blog/post_update.html', context)


def post_delete(request, pk):
    post = Post.objects.filter(author=request.user)
    post.delete()
    return redirect('my_posts')


def rate_post(request, pk, rate):
    post = Post.objects.filter(id=pk).first()
    not_anonymous = not (isinstance(request.user, AnonymousUser))
    try:
        rated_before = Rating.objects.filter(post=post, profile=request.user)
    except TypeError:
        messages.error(request, 'You should login first')
        return redirect('login')

    if not_anonymous and not rated_before:
        rating = Rating(
            post=post, profile=request.user,
            rating=rate, rated=True
        )
        rating.save()
        messages.success(request, 'Your rating have been saved')
    else:
        messages.error(request, 'You have rated before')
        return redirect('main_page')

    stars = Rating.objects.filter(post=post)
    points = reduce(lambda x, y: x + y, [i.rating for i in stars])
    final_rating = math.ceil(points/len(stars))
    post.rating = final_rating
    post.save()

    return redirect('main_page')
