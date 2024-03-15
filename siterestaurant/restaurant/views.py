from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.template.loader import render_to_string


menu = [{'title': "Главная", 'url_name': ''},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить отзыв", 'url_name': 'addpage'},
        {'title': "Просмотреть отзывы", 'url_name': 'contact'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]
data_db = [
    {'id': 1, 'dish': 'Стейк', 'category': 1, 'author': 'Иванов Петр',
     'review': 'Отличное блюдо, порции большие, всем рекомендую!', 'time': '2022-10-15 14:30', 'is_published': True},
    {'id': 2, 'dish': 'Паста', 'category': 2, 'author': 'Сидорова Ольга',
     'review': 'Понравилось всем в семье, приятное обслуживание.', 'time': '2022-10-16 18:45', 'is_published': True},
    {'id': 3, 'dish': 'Салат', 'category': 1, 'author': 'Петров Игорь',
     'review': 'Не впечатлило, цена не соответствует качеству.', 'time': '2022-10-17 12:15', 'is_published': False},
    {'id': 4, 'dish': 'Суп', 'category': 1, 'author': 'Козлова Мария', 'review': 'Очень вкусно, придем еще раз!',
     'time': '2022-10-18 20:00', 'is_published': True},
    {'id': 5, 'dish': 'Десерт', 'category': 3, 'author': 'Смирнов Алексей',
     'review': 'Блюдо было горячим и свежим, отличный выбор.', 'time': '2022-10-19 17:30', 'is_published': True},
    {'id': 6, 'dish': 'Рыба', 'category': 2, 'author': 'Кузнецова Елена',
     'review': 'Слишком много соли, не понравилось.', 'time': '2022-10-20 13:45', 'is_published': True},
    {'id': 7, 'dish': 'Бургер', 'category': 2, 'author': 'Васильев Дмитрий',
     'review': 'Сервис на высоте, блюда вкусные.', 'time': '2022-10-21 19:15', 'is_published': True},
    {'id': 8, 'dish': 'Пицца', 'category': 2, 'author': 'Павлова Анна',
     'review': 'Не оправдало ожиданий, среднее качество.', 'time': '2022-10-22 11:20', 'is_published': False},
    {'id': 9, "dish": "Шашлык", "category": 2, "author": "Михайлов Кирилл",
     "review": "Блюдо приготовлено аккуратно, вкусно.", "time": "2022-10-23 16:40", "is_published": True},
    {'id': 10, "dish": "Сэндвич", "category": 2, "author": "Григорьева Людмила",
     "review": "Отличное сочетание ингредиентов, рекомендую.", "time": "2022-10-24 21:00", "is_published": True},
    {'id': 11, "dish": "Суп", "category": 1, "author": "Орлов Сергей",
     "review": "Цена невысокая, но качество соответствует.", "time": "2022-10-25 15:10", "is_published": True},
    {'id': 12, "dish": "Стейк", "category": 1, "author": "Никитина Алена",
     "review": "Быстрое обслуживание, приятный вкус.", "time": "2022-10-26 18:30", "is_published": True},
    {'id': 13, "dish": "Паста", "category": 2, "author": "Исаев Даниил",
     "review": "Порции маленькие, но очень вкусно.", "time": "2022-10-27 12:45", "is_published": True},
    {'id': 14, "dish": "Рыба", "category": 2, "author": "Федорова Екатерина",
     "review": "Неожиданно хорошее качество за такую цену.", "time": "2022-10-28 19:50", "is_published": True},
    {'id': 15, "dish": "Десерт", "category": 4, "author": "Попов Владимир",
     "review": "Очень понравилось, буду рекомендовать друзьям.", "time": "2022-10-29 16:20", "is_published": True},
    {'id': 16, "dish": "Бургер", "category": 2, "author": "Соколова Татьяна",
     "review": "Замечательный выбор блюд на любой вкус.", "time": "2022-10-30 20:30", "is_published": True}
]

cats_db = [
    {'id': 1, 'name': 'Первое'},
    {'id': 2, 'name': 'Второе'},
    {'id': 3, 'name': 'Десерты'},
    {'id': 4, 'name': 'Напитки'},
]


# def index(request):
#     return HttpResponse("Страница приложения restaurant.")


class MyClass:
    def __init__(self, a, b):
        self.a = a
        self.b = b


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': data_db,
        'cats': cats_db,
        'cat_selected': 0,
    }
    return render(request, 'restaurant/index.html', context=data)


def about(request):
    return render(request, 'restaurant/about.html', {'title': 'О сайте', 'menu': menu})


def add(request):
    return render(request, 'restaurant/add.html', {'title': 'Добавление отзыва', 'menu': menu})


def look(request):
    data = {
        'title': 'Отзывы',
        # 'menu': menu,
        'posts': data_db,
        'cats': cats_db,
        # 'cat_selected': 0,  # не обязательная строчка
    }
    return render(request, 'restaurant/look.html', context=data)

def show_category(request, cat_id):
    data = {
        'title': 'Отображение по рубрикам',
        # 'menu': menu,
        'posts': data_db,
        'cat_selected': cat_id,
    }
    return render(request, 'restaurant/cats.html', context=data)


def login(request):
    return HttpResponse("Авторизация")


def show_post(request, post_id):
    return HttpResponse(f"Отображение отзыва с id ={post_id}")


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')




