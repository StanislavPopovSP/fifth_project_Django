# Какой-то дополнительный функционал
from .models import *

# Пункты меню
menu = [
    {'title': 'Добавить статью', 'url_name': 'add_page'},  # url_name - будет лежать путь, если будет пусто будет ошибка, т.к ни чего не существует.
    {'title': 'Войти', 'url_name': 'index'}
]  # добавим пункты меню


class DataMixin:
    """Убираем дублирование кода"""

    def get_user_context(self, **kwargs):  # создадим контекст для шаблона
        context = kwargs # kwargs - в него будут приходить принимаемые аргументы
        cats = Category.objects.all()  # все категории

        context['menu'] = menu  # в конетексте у каждого пункта используется меню
        context['cats'] = cats  # к каждой статье принимается категория

        if 'cat_selected' not in context:  # если выделенная категория не находится в context
            context['cat_selected'] = 0  # категория не активная
        return context
