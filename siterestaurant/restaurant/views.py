import uuid

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

    #
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     # 'posts': Restaurant.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }

    def get_context_data(self, *, object_list=None, **kwargs):
        return self.get_mixin_context(super().get_context_data(**kwargs), title='Главная страница', cat_selected=0, )

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = 'Главная страница'
    #     context['menu'] = menu
    #     context['cat_selected'] = 0
    #     return context

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     # return self.get_mixin_context(super().get_context_data(**kwargs), title='Главная страница', menu=menu, cat_selected=0, )
    #     context = super().get_context_data(**kwargs)
    #     return self.get_mixin_context(context, title='Главная страница', menu=menu, cat_selected=0)

    def get_queryset(self):
        return Restaurant.published.all().select_related('cat')
    # template_name = 'restaurant/index.html'
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts':
    #         Restaurant.published.all().select_related('cat'),
    #     'cat_selected': 0,
    # }


class RestaurantCategory(DataMixin, ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context, title='Категория - ' + cat.name, cat_selected=cat.id, )

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     cat = context['posts'][0].cat
    #     context['title'] = 'Категория - ' + cat.name
    #     context['menu'] = menu
    #     context['cat_selected'] = cat.id
    #     return context

    def get_queryset(self):
        return (Restaurant.published.filter(cat__slug=self.kwargs['cat_slug']).
                select_related('cat'))


class TagPostList(DataMixin, ListView):
    template_name = 'restaurant/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title='Тег: ' + tag.tag)

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
    #     context['title'] = 'Тег: ' + tag.tag
    #     context['menu'] = menu
    #     context['cat_selected'] = None
    #     return context

    def get_queryset(self):
        return (Restaurant.published.filter(tags__slug=self.kwargs['tag_slug']).
                select_related('cat'))


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
    contact_list = Restaurant.published.all()
    paginator = Paginator(contact_list, 3)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # if request.method == "POST":
    #     form = UploadFileForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         handle_uploaded_file(form.cleaned_data['file'])
    # else:
    #     form = UploadFileForm()
    return render(request, 'restaurant/about.html',
                  {'page_obj': page_obj, 'title': 'О сайте'})


# class AddPoll(View):
#     def get(self, request):
#         form = AddPollForm()
#         return render(request, 'restaurant/addpoll.html',
#                       {'menu': menu, 'title': 'Добавление отзыва', 'form':
#                           form})
#
#     def post(self, request):
#         form = AddPollForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             form.save()
#             return redirect('home')
#         return render(request, 'restaurant/addpoll.html',
#                       {'menu': menu, 'title': 'Добавление отзыва', 'form':
#                           form})
#

# class AddPoll(FormView):
#     form_class = AddPollForm
#     template_name = 'restaurant/addpoll.html'
#     success_url = reverse_lazy('home')
#     extra_context = {
#         'menu': menu,
#         'title': 'Добавление статьи',
#     }
#
#     def form_valid(self, form):
#         form.save()
#         return super().form_valid(form)


class AddPoll(DataMixin, CreateView):
    model = Restaurant
    # fields = ['title', 'slug', 'content',
    #           'is_published', 'cat']
    fields = '__all__'
    # form_class = AddPostForm
    template_name = 'restaurant/addpoll.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление отзыва'

    # model = Restaurant
    # # form_class = AddPollForm
    # fields = '__all__'
    # template_name = 'restaurant/addpoll.html'
    # success_url = reverse_lazy('home')
    # extra_context = {
    #     'menu': menu,
    #     'title': 'Добавление отзыва',
    # }


class UpdatePoll(UpdateView):
    model = Restaurant
    # fields = ['title', 'content', 'photo',
    #           'is_published', 'cat']

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


# class DeletePoll(DeleteView):
#     model = Restaurant
#     # fields = ['title', 'content', 'photo',
#     #           'is_published', 'cat']
#     success_url = reverse_lazy('author-list')
#     template_name_suffix = '_confirm_delete'
#     title_page = 'Удаление  отзыва'
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Delete Author'
#         return context


def addPoll(request):
    if request.method == 'POST':
        form = AddPollForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = AddPollForm()

    return render(request, 'restaurant/addpoll.html',
                  {'menu': menu, 'title': 'Добавление отзыва', 'form': form})


def look(request):
    # contact_list = Restaurant.published.all()
    # paginator = Paginator(contact_list, 3)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)
    data = {
        'title': 'Отзывы',
        # 'menu': menu,
        'posts': Restaurant.published.all(),
        'cats': cats_db,
        # 'page_obj': page_obj,
        # 'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'restaurant/look.html',  context=data)


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


class ShowPost(DataMixin, DetailView):
    model = Restaurant
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    template_name = 'restaurant/post.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title='Отзыв от: ')

    # title = context['post']

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['title'] = context['post']
    #     context['menu'] = menu
    #     return context

    def get_object(self, queryset=None):
        return get_object_or_404(Restaurant.published,
                                 slug=self.kwargs[self.slug_url_kwarg])


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
