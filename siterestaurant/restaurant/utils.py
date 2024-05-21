menu = [{'title': "Главная", 'url_name': ''},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить отзыв", 'url_name': 'addpage'},
        {'title': "Просмотреть отзывы", 'url_name': 'contact'},
        {'title': "Обратная связь", 'url_name': 'contact'},
        {'title': "Войти", 'url_name': 'login'}
        ]


class DataMixin:
    title_page = None
    paginate_by = 2
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'menu' not in self.extra_context:
            self.extra_context['menu'] = menu

    def get_mixin_context(self, context, **kwargs):
        context['menu'] = menu
        context.update(kwargs)
        return context

