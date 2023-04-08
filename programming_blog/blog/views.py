from django.shortcuts import render
from django.views.generic import ListView  # он за нас сделает большую работу, не надо будет указывать много элементов одновременно.
from django.views.generic import DetailView # детальное описание какого то View
from .models import *

menu = [
    {'title': 'Добавить статью', 'url_name': 'index'}, # url_name - будет лежать путь, если будет пусто будет ошибка, т.к ни чего не существует.
    {'title': 'Войти', 'url_name': 'index'} #
] # добавим пункты меню

# если работаем с классом, то без модели он работать не может
class BlogHome(ListView):
    """Обработка главной страницы"""
    model = Blog
    template_name = 'blog/index.html' # куда будет выводиться HTML страница. template_name - как свойства в классе, они имеют определенное значение, что мы в них должны поместить. В Django есть стандартные названия шаблонов.
    context_object_name = 'posts' # Имя объекта внутри шаблона. Специальная переменная которая будет выводить код в html шаблон. Берет данные из модели.

    def get_context_data(self, *, object_list=None, **kwargs): # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Данные для вывода"""
        context = super().get_context_data(**kwargs) # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        context['title'] = 'Главная страница' # на главную страницу добавляем заголовок
        context['cat_selected'] = 0 # придумали название cat_selected и его значение 0
        context['menu'] = menu # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        return context

    def get_queryset(self): # Верните список элементов для этого представления. Возвращаемое значение должно быть итеративным и может быть экземпляром QuerySet
        """Делаем ограничения, возвращаем нужные данные, связываем публикацию с категорией"""
        return Blog.objects.filter(is_published=True).select_related('cat') # если статья опубликована. Берем из БД Blog только те записи которые будут опубликованы. select_related('cat') - связано с категорией из модели.


class ShowPost(DetailView):
    """Просмотр отдельной статьи"""
    model = Blog # с какой моделью работаем
    template_name = 'blog/post.html' # имя шаблона
    slug_url_kwarg = 'post_slug' # имя slug из пути
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs): # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Данные для вывода"""
        context = super().get_context_data(**kwargs) # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        context['title'] = context['post'] # В каждой статье будет название свое конкретное. context[] - в контекст передадим post, что бы попадало имя конкретной статьи в title.
        context['menu'] = menu # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        return context

class BlogCategory(ListView):
    """Категория определенной статьи"""
    model = Blog  # с какой моделью работаем
    template_name = 'blog/index.html'  # имя шаблона
    context_object_name = 'posts' # имя slug из пути
    allow_empty = False # не разрешим выводить пустые категории
    # есть статьи хот-е опубликованы либо нет, надо выводить только опубликованные статьи.
    def get_queryset(self): # Верните список элементов для этого представления. Возвращаемое значение должно быть итеративным и может быть экземпляром QuerySet
        """Делаем ограничения, возвращаем нужные данные, связываем публикацию с категорией"""
        return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat') # в виде ключа передадим self.kwargs['cat_slug']

    def get_context_data(self, *, object_list=None, **kwargs): # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Данные для вывода"""
        context = super().get_context_data(**kwargs) # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        context['title'] = 'Категория - ' + str(context['posts'][0].cat)# на главную страницу добавляем заголовок
        context['cat_selected'] = context['posts'][0].cat_id # так как slug идёт уникальным, ему проще найти по id элемент.
        context['menu'] = menu # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        return context