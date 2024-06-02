import uuid

from django.conf import settings
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView

from restaurant.forms import AddPollForm, UploadFileForm
from restaurant.models import Restaurant, Category, TagPost, UploadFiles
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView

from restaurant.utils import *

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


class RestaurantHome(DataMixin, ListView):
    model = Restaurant
    context_object_name = 'posts'
    template_name = 'restaurant/index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, title='Главная страница', cat_selected=0)
        context['default_poll_image'] = settings.DEFAULT_POLL_IMAGE
        return context

    def get_queryset(self):
        return Restaurant.published.all().select_related('cat')


class RestaurantCategory(DataMixin, ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'posts'
    allow_empty = False
    default_poll_image = settings.DEFAULT_POLL_IMAGE,

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        context = self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id)
        context['default_poll_image'] = settings.DEFAULT_POLL_IMAGE
        return context

    def get_queryset(self):
        return (Restaurant.published.filter(cat__slug=self.kwargs['cat_slug']).
                select_related('cat'))


def handle_uploaded_file(f):
    name = f.name
    ext = ''
    if '.' in name:
        ext = name[name.rindex('.'):]
        name = name[:name.rindex('.')]
    suffix = str(uuid.uuid4())
    with open(f"uploads/{name}_{suffix}{ext}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def about(request):
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            fp = UploadFiles(file=form.cleaned_data['file'])
            fp.save()
    else:
        form = UploadFileForm()

    return render(request, 'restaurant/about.html',
                  {'title': 'О сайте', 'menu': menu, 'form': form})


class UpdatePage:
    pass


class AddPoll(LoginRequiredMixin, DataMixin, CreateView, PermissionRequiredMixin):
    permission_required = 'restaurant.add_restaurant'
    model = Restaurant
    form_class = AddPollForm
    template_name = 'restaurant/addpoll.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление отзыва'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePoll(UpdateView, UpdatePage):
    permission_required = 'restaurant.change_restaurant'
    model = Restaurant
    fields = ['dish', 'review', 'is_published', 'cat', 'contact', 'photo']
    template_name = 'restaurant/addpoll.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование отзыва'


class DeletePoll(DataMixin, DeleteView):
    model = Restaurant
    template_name = 'restaurant/delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление отзыва'
    extra_context = {
        'menu': menu,
        'title': 'Удаление отзыва',
    }


@login_required
def look(request):
    data = {
        'title': 'Отзывы',
        'posts': Restaurant.published.all(),
        'cats': cats_db,
        'default_poll_image': settings.DEFAULT_POLL_IMAGE,
    }
    return render(request, 'restaurant/look.html', context=data)



def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    posts = tag.tags.filter(is_published=Restaurant.Status.PUBLISHED)
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'cat_selected': None,
        'default_poll_image': settings.DEFAULT_POLL_IMAGE,
    }
    return render(request, 'restaurant/index.html', context=data)


def login(request):
    return HttpResponse("Авторизация")


class ShowPost(DataMixin, DetailView):
    model = Restaurant
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'restaurant/post.html'
    extra_context = {
        'default_poll_image': settings.DEFAULT_POLL_IMAGE,
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = self.get_mixin_context(context, title='Отзыв от:')
        context['default_poll_image'] = settings.DEFAULT_POLL_IMAGE
        return context

    def get_object(self, queryset=None):
        return get_object_or_404(Restaurant.published,
                                 slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
