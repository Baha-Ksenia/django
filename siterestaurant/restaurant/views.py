from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string

from restaurant.models import Restaurant, Category, TagPost

menu = [{'title': "Главная", 'url_name': ''},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить отзыв", 'url_name': 'addpage'},
        {'title': "Просмотреть отзывы", 'url_name': 'contact'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]

cats_db = [
    {'id': 1, 'name': 'Первое'},
    {'id': 2, 'name': 'Второе'},
    {'id': 3, 'name': 'Десерты'},
    {'id': 4, 'name': 'Напитки'},
]


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):
    posts = Restaurant.published.all()
    data = {
        'title': 'Главная страница',
        # 'menu': menu,
        'posts': posts,
        'cat_selected': 0,
    }
    return render(request, 'restaurant/index.html',
                  context=data)


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'О сайте', 'menu': menu})


def add(request):
    return render(request, 'restaurant/add.html', {'title': 'Добавление отзыва', 'menu': menu})


def look(request):
    data = {
        'title': 'Отзывы',
        # 'menu': menu,
        'posts': Restaurant.published.all(),
        'cats': cats_db,
        # 'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'restaurant/look.html', context=data)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    posts = Restaurant.published.filter(cat_id=category.pk)
    data = {
        'title': f'Рубрика: {category.name}',
        # 'menu': menu,
        'posts': posts,
        'cat_selected': category.pk,
    }
    return render(request, 'restaurant/cats.html',
                  context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Restaurant.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
    }
    return render(request, 'restaurant/index.html', context=data)


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_slug):
    post = get_object_or_404(Restaurant, slug=post_slug)

    data = {
        'title': 'Отзыв от:',
        # 'menu': menu,
        'post': post,
        'cats': cats_db,
        # 'cat_selected': 1,
    }
    return render(request, 'restaurant/post.html',
                  context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
