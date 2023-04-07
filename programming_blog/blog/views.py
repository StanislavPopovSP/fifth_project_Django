from django.shortcuts import render
from django.views.generic import ListView  # он за нас сделает большую работу, не надо будет указывать много элементов одновременно.
from .models import *

menu = [
    {'title': 'Добавить статью', 'url_name': 'index'}, # url_name - будет лежать путь, если будет пусто будет ошибка, т.к ни чего не существует.
    {'title': 'Войти', 'url_name': 'index'} #
] # добавим пункты меню

# если работаем с классом, то без модели он работать не может
class BlogHome(ListView):
    model = Blog
    template_name = 'blog/index.html' # куда будет выводиться HTML страница. template_name - как свойства в классе, они имеют определенное значение, что мы в них должны поместить.
    context_object_name = 'posts' # Имя объекта внутри шаблона. Специальная переменная которая будет выводить код в html шаблон.

    def get_context_data(self, *, object_list=None, **kwargs): # данный метод сущ-ет для любого класса который наследуется от ListView.
        context = super().get_context_data(**kwargs) # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        context['title'] = 'Главная страница' # на главную страницу добавляем заголовок
        context['menu'] = menu # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        return context