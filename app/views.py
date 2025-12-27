"""
Definition of views.
"""

from datetime import datetime

from django.contrib.auth.forms import UserCreationForm
from django.http import HttpRequest
from django.shortcuts import render, redirect

from .forms import FeedbackForm, CommentForm, BlogForm
from .models import Blog, Comment, Feedback



def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title': 'Домашняя страница',
            'year': datetime.now().year,
        }
    )


def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Контакты',
            'message': 'Свяжитесь с нами удобным для Вас способом',
            'year': datetime.now().year,
        }
    )


def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'О нас',
            'message': 'Информация о ArtSisters',
            'year': datetime.now().year,
        }
    )


def pool(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("pool")
    else:
        form = FeedbackForm()

    reviews = Feedback.objects.all()[:12]  # последние 12

    return render(request, "app/pool.html", {
        "title": "Обратная связь",
        "message": "Пожалуйста, оцените сайт ArtSisters и оставьте пожелания.",
        "form": form,
        "reviews": reviews,
        "year": datetime.now().year,
    })



def registration(request):
    """Renders the registration page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()
            reg_f.save()
            return redirect('home')
    else:
        regform = UserCreationForm()

    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            'year': datetime.now().year,
        }
    )


# список статей 
def blog(request):
    posts = Blog.objects.all().order_by('-posted')
    return render(request, 'app/blog.html', {
        'title': 'Блог',
        'posts': posts,
        'year': datetime.now().year,
    })


# статья + комментарии
def blogpost(request, parametr):
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr).order_by('-date')

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect('login')
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = post_1
            comment_f.save()
            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post': post_1,
            'comments': comments,
            'form': form,
            'year': datetime.now().year,
        }
    )


# добавление статьи
def newpost(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return redirect('home')

    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('blog')
    else:
        form = BlogForm()

    return render(request, 'app/newpost.html', {
        'title': 'Новая статья',
        'form': form,
        'year': datetime.now().year,
    })


# видево
def videopost(request):
    return render(request, 'app/videopost.html', {
        'title': 'Видео',
        'year': datetime.now().year,
    })
