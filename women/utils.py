from django.db.models import Count

from .models import *


menu = [{'title': 'Про сайт', 'url_name': 'about'},
        {'title': 'Добавити статтю', 'url_name': 'add_page'},
        {'title': 'Відгук', 'url_name': 'contact'},
        {'title': 'Гра', 'url_name': 'rooms'},
        {'title': 'Чат', 'url_name': 'chat_rooms'},
        ]


class DataMixin:
    paginate_by = 3

    def get_user_context(self, **kwargs):
        context = kwargs
        cats = Category.objects.annotate(Count('women'))
        context['cats'] = cats

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        if 'cat_selected' not in context:
            context['cat_selected'] = 0
        return context
