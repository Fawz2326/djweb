"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest
from .forms import FeedbackForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from django.db import models
from .models import Blog
from .forms import BlogForm

from .models import Comment
from .forms import CommentForm
from .models import Category
from .models import Cart, CartItem, Product

def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

def links(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/links.html',
        {
            'title':'Полезные ссылки',
            'year':datetime.now().year,
        }
    )

def feedback(request):
    assert isinstance(request, HttpRequest) 
    data = None
    gender = {'1': 'Мужчина', '2': 'Женщина'}
    age = {'1': 'Меньше 18', '2': 'От 18 до 21', '3': 'Больше 21'}
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['gender'] = gender[ form.cleaned_data['gender'] ] 
            data['age'] = age[ form.cleaned_data['age'] ] 
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Дa'
            else:
                data['notice'] = 'Heт'
            data['email'] = form.cleaned_data['email'] 
            data['message'] = form.cleaned_data['message'] 
            form = None
    else:
        form = FeedbackForm()
    return render( request,
           'app/pool.html',
           {
              'form': form,
              'data' :data
           }
    )

def registration(request):
    """Renders the registration page."""
    if request.method == "POST":
        regform = UserCreationForm(request.POST)
        if regform.is_valid():
            reg_f = regform.save(commit=False)
            reg_f.is_staff = False
            reg_f.is_active = True
            reg_f.is_superuser = False
            reg_f.date_joined = datetime.now()
            reg_f.last_login = datetime.now()

            regform.save()

            return redirect('home')
    else:
        regform = UserCreationForm()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform,
            
            'year': datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    posts = Blog.objects.all()

    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts,
            'year':datetime.now().year,
        }
    )

def blogpost(request, parametr):
    """Renders the blog page."""
    
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr)
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user
            comment_f.date = datetime.now()
            comment_f.post = Blog.objects.get(id=parametr)
           #comment_f.image = request.FILES['image'] # имя поля для загрузки изображения
            comment_f.save()

            return redirect('blogpost', parametr=post_1.id)
    else:
        form = CommentForm()

    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1,

            'comments': comments,
            'form': form,

            'year':datetime.now().year,
        }
    )

def newpost(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST":
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.author = request.user
            #
            blog_f.save()

            return redirect('blog')
    else:
        blogform = BlogForm()

    return render(
        request,
        'app/newpost.html',
        {
            'blogform': blogform,
            'title': 'Добавить статью блога',
            
            'year': datetime.now().year
        }
    )

def videopost(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Видео',
            'year':datetime.now().year,
        }
    )

def catalog(request):
    categories = Category.objects.prefetch_related('products').all()
    context = {
        'categories': categories,
        'title': 'Каталог товаров',
        'message': 'Добро пожаловать в наш интернет-магазин!'
    }
    return render(request, 'app/catalog.html', context)

#@login_required
def cart(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправление на страницу входа
    items = CartItem.objects.filter(user=request.user)
    total_cart_price = sum(item.total_price() for item in items)
    return render(request, 'app/cart.html', {
        'items': items,
        'total_cart_price': total_cart_price,
    })

#@login_required
def add_to_cart(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Перенаправление на страницу входа
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(
        product=product,
        user=request.user,
        #defaults={'quantity': 1}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    return redirect('cart')

def update_cart_quantity(request, item_id):
    if request.method == "POST":
        item = get_object_or_404(CartItem, id=item_id)
        action = request.POST.get("action")

        if action == "increase":
            item.quantity += 1  # Увеличиваем количество
        elif action == "decrease" and item.quantity > 1:
            item.quantity -= 1  # Уменьшаем количество, но не меньше 1
        elif action == "delete":
            item.delete()  # Удаляем товар из корзины

        if action != "delete":  # Сохраняем только для увеличения/уменьшения
            item.save()
    return redirect('cart')  # Возвращаемся на страницу корзины