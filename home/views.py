from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
# Create your views here.
def index(request):
    username = request.user.username
    posts = list(Post.objects.all())
    posts = posts[::-1]
    context = {'username': username, 'posts':posts}
    return render(request, 'index.html', context=context)

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username1')
        password = request.POST.get('password1')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            context = {'msg1': 'Invalid Credentials.'}
            return render(request, 'index.html', context=context)
    return redirect('index')

def signup_user(request):
    if request.method == "POST":
        username = request.POST.get('username2')
        email = request.POST.get('email')
        password = request.POST['password2']
        try:
            user = User.objects.get(username=username)
            if user is not None:
                context = {'msg2': 'Username Already Taken.'}
                return render(request, 'index.html', context=context)
        except Exception as e:
            user = None
        try:
            user = User.objects.get(email=email)
            if user is not None:
                context = {'msg2': 'Email Already Taken.'}
                return render(request, 'index.html', context=context)
        except Exception as e:
            user = None
        user = User.objects.create_user(username, email, password)
        user.set_password(password)
        user.save()
        context = {'msg2': 'Signed Up Successfully. Please Login.'}
        return render(request, 'index.html', context=context)
    return redirect('index')

def share(request):
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        username = request.user
        user = User.objects.get(username=username)
        post = Post(title=title, content=content, user=user)
        post.save()
        return redirect('index')
    return redirect('index')

def logout_user(request):
    logout(request)
    return redirect('index')

def my_posts(request):
    username = request.user.username
    user = User.objects.get(username=username)
    posts = list(Post.objects.filter(user=user))
    posts = posts[::-1]
    context = {'username': username, 'posts':posts}
    return render(request, 'my_posts.html', context=context)

def edit_post(request, id):
    post = Post.objects.get(id=id)
    if request.method=="POST":
        title = request.POST['title']
        content = request.POST['content']
        post.title = title
        post.content = content
        post.save()
        return redirect('my-posts')
    username = request.user.username
    context = {'username': username, 'post':post}
    return render(request, 'my_posts.html', context)

def delete_post(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect('my-posts')

def search(request):
    if request.method=="POST":
        key = request.POST['key']
        posts = list(set(list(Post.objects.filter(title__contains=key)) + list(Post.objects.filter(content__contains=key))))
        username = request.user.username
        posts = posts[::-1]
        context = {'username': username, 'posts':posts, 'key':key}
        return render(request, 'index.html', context=context)