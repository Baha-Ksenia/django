menu = [{'title': "Главная", 'url_name': 'home'},
        {'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить отзыв", 'url_name': 'addPoll'},
        {'title': "Просмотреть отзывы", 'url_name': 'look'},
        ]


class DataMixin:
    title_page = None
    paginate_by = 3
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page


    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context

