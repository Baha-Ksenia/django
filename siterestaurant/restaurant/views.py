from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string


# def index(request):
#     return HttpResponse("Страница приложения restaurant.")
def index(request):
    return render(request, 'restaurant/index.html')


def about(request):
    return render(request, 'women/about.html')


def categories(request, cat_id):
    return HttpResponse("<h1>Категории блюд</h1><p >id:{cat_id}</p>")


def categories_by_slug(request, cat_slug):
    if request.GET:
        print(request.GET)
    return HttpResponse(f"<h1>Статьи по категориям</h1><p >slug: {cat_slug}</p>")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


def archive(request, year):
    if year > 2024:
        return redirect(index, permanent=True)
        # return HttpResponseRedirect('/')
    return HttpResponse(f"<h1>Архив отзывов по годам</h1><p> {year} </p> ")


def add_feedback(request):
    return HttpResponse("<h1>Страница нового отзыва</h1>")
