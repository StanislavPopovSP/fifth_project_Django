# Какой-то дополнительный функционал
from .models import *
from django.db.models import Count  # Считает кол-во элементов

# Пункты меню
menu = [
    {'title': 'Добавить статью', 'url_name': 'add_page'},  # url_name - будет лежать путь, если будет пусто будет ошибка, т.к ни чего не существует.
    {'title': 'Войти', 'url_name': 'index'}
]  # добавим пункты меню


class DataMixin:
    """Убираем дублирование кода"""
    paginate_by = 3

    def get_user_context(self, **kwargs):  # создадим контекст для шаблона
        context = kwargs  # kwargs - в него будут приходить принимаемые аргументы
        cats = Category.objects.annotate(Count('blog'))  # Пускай считает кол-во элементов в блоге, annotate - связывает блог с категорией и считаем кол-во элементов в блоке.
        user_menu = menu.copy()  # получаем копию словаря
        if not self.request.user.is_authenticated:  # если пользователь не аутентифицирован, удаляем 'title': 'Добавить статью'
            user_menu.pop(0)

        context['menu'] = user_menu  # в конетексте у каждого пункта используется меню
        context['cats'] = cats  # к каждой статье принимается категория

        if 'cat_selected' not in context:
            context['cat_selected'] = 0

        return context
