from django.views.generic import ListView  # он за нас сделает большую работу, не надо будет указывать много элементов одновременно.
from django.views.generic import DetailView  # детальное описание какого то View
from django.views.generic import CreateView  # создать представление(обработчик)
from django.views.generic import FormView  # для создания формы обратной связи
from django.urls import reverse_lazy  # это как redirect в функциях перенаправление, что бы когда заполнили элементы формы, могли перейти на какую-то определенную страницу.
from django.contrib.auth.mixins import LoginRequiredMixin # Готовый Mixin Django для ограничения доступа к страницам, например для не авторизированных пользователей. Работа авторизацией.
from django.contrib.auth.views import LoginView # Что бы залогиниться
from django.contrib.auth.forms import AuthenticationForm # Для аутентификации, готовая форма
from django.shortcuts import redirect # для перенаправления
from django.contrib.auth import login # что бы авторизоваться автоматически
from django.core.mail import send_mail, BadHeaderError # BadHeaderError - ошибка
from django.http import HttpResponse
from .utils import *
from .forms import *


# Если работаем с классом, то без модели он работать не может.
class BlogHome(DataMixin, ListView):
    """Обработка главной страницы"""
    model = Blog
    template_name = 'blog/index.html'  # куда будет выводиться HTML страница. template_name - как свойства в классе, они имеют определенное значение, что мы в них должны поместить. В Django есть стандартные названия шаблонов.
    context_object_name = 'posts'  # Имя объекта внутри шаблона. Специальная переменная которая будет выводить код в html шаблон. Берет данные из модели.

    def get_context_data(self, *, object_list=None, **kwargs):  # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Получаем данные для шаблона """
        context = super().get_context_data(**kwargs)  # get_context_data есть у родительского класса, получаем доступ к такому же get_context_data со всеми ключами и значениями.
        # context['title'] = 'Главная страница'  # на главную страницу добавляем заголовок
        # context['cat_selected'] = 0  # придумали название cat_selected и его значение 0
        # context['menu'] = menu  # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        # return context
        c_def = self.get_user_context(title='Главная страница')
        return dict(list(context.items()) + list(c_def.items()))


    def get_queryset(self) -> list:  # Верните список элементов для этого представления. Возвращаемое значение должно быть итеративным и может быть экземпляром QuerySet
        """Делаем ограничения, возвращаем нужные данные, связываем публикацию с категорией"""
        return Blog.objects.filter(is_published=True).select_related('cat')  # если статья опубликована. Берем из БД Blog только те записи которые будут опубликованы. select_related('cat') - связано с категорией из модели.


class ShowPost(DataMixin, DetailView):
    """Просмотр отдельной статьи"""
    model = Blog  # с какой моделью работаем
    template_name = 'blog/post.html'  # имя шаблона
    slug_url_kwarg = 'post_slug'  # имя slug из пути
    context_object_name = 'post'

    def get_context_data(self, *, object_list=None, **kwargs):  # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Получаем данные для шаблона"""
        context = super().get_context_data(**kwargs)
        # context['title'] = context['post']  # В каждой статье будет название свое конкретное. context[] - в контекст передадим post, что бы попадало имя конкретной статьи в title.
        # context['menu'] = menu  # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        # return context
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class BlogCategory(DataMixin, ListView):
    """Категория определенной статьи"""
    model = Blog
    template_name = 'blog/index.html'
    context_object_name = 'posts'
    allow_empty = False  # не разрешим выводить пустые категории

    # есть статьи хот-е опубликованы либо нет, надо выводить только опубликованные статьи.
    def get_queryset(self) -> list:  # Верните список элементов для этого представления. Возвращаемое значение должно быть итеративным и может быть экземпляром QuerySet
        """Делаем ограничения, возвращаем нужные данные, связываем публикацию с категорией, переопределяем доступ к БД."""
        return Blog.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True).select_related('cat')  # в виде ключа передадим self.kwargs['cat_slug']
        # or
        # return Blog.objects.filter(cat__slug=self.kwargs.get('cat_slug'), is_published=True).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):  # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Данные для вывода"""
        context = super().get_context_data(**kwargs)  # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        # context['title'] = 'Категория - ' + str(context['posts'][0].cat)  # на главную страницу добавляем заголовок
        # context['cat_selected'] = context['posts'][0].cat_id  # так как slug идёт уникальным, ему проще найти по id элемент.
        # context['menu'] = menu  # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        # return context
        c = Category.objects.get(slug=self.kwargs['cat_slug']) # В виде ключа будем брать cat_slug какой-то категории (Аргумент, поле таблицы slug берем его cat_slug)
        c_def = self.get_user_context(title='Категория - ' + str(c.name), cat_selected=c.pk)
        return dict(list(context.items()) + list(c_def.items()))

# Мы хотим что бы на страницу добавить статью, заходили только авторизированные пользователи.
class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    """Обработка формы добавления статьи"""
    form_class = AddPostForm  # это готовое имя, его не придумываем. Что бы мы могли сделать свою форму.
    template_name = 'blog/addpage.html'  # какой шаблон будет заниматься обработкой текущей страницей.
    success_url = reverse_lazy('index')  # если зашли на эту страницу и отправили данные формы, они у нас отправились удачно, добавляется success_url. Через reverse_lazy перенаправит на какую-то страницу.
    # 1 Вариант, ошибка
    # raise_exception = True # если пользователь не авторизирован Буде генерироваться ошибка 403 Forbidden
    # 2 второй перенаправление на какую то страницу.
    login_url = reverse_lazy('index') # Когда незарегистрированный пользователь попытается зайти на добавить статью, то его перенаправит на главную страницу

    def get_context_data(self, *, object_list=None, **kwargs):  # данный метод сущ-ет для любого класса который наследуется от ListView.
        """Получаем данные для шаблона"""
        context = super().get_context_data(**kwargs)  # контекст есть у родительского класса, получаем context для шаблона со всеми ключами и значениями.
        # context['title'] = 'Добавление статьи'  # в заголовке окна браузера будет выводится.
        # context['menu'] = menu  # Что бы их можно было увидеть # Когда обратимся к ключу 'menu' получим доступ к menu.
        c_def = self.get_user_context(title='Добавление статьи')
        return dict(list(context.items()) + list(c_def.items()))

class RegisterUser(DataMixin, CreateView):
    """Регистрация пользователя, обработка формы"""
    form_class = RegisterUserForm
    template_name = 'blog/register.html'
    # success_url = reverse_lazy('login') # данный переход нужен если не делать form_valid

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        """Переопределяем данный метод"""
        user = form.save() # сохраняем форму и получаем пользователя
        login(self.request, user) # после регистрации автоматически залогинились и перешли на страницу index
        return redirect('index') # Что бы когда зарегистрировались, мы автоматически перешли через страницу авторизаии, что бы на нее не попали.


class LoginUser(DataMixin, LoginView):
    """Авторизирует пользователя"""
    form_class = AuthenticationForm
    template_name = 'blog/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Авторизация')
        return dict(list(context.items()) + list(c_def.items()))


class ContactFormView(DataMixin, FormView):
    """Обработка формы обратной связи"""
    form_class = ContactForm # Будем создавать свою форму
    template_name = 'blog/contact.html'
    success_url = reverse_lazy('index')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Обратная связь')
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        """Отправка письма на почту"""
        print(form.cleaned_data) # cleaned_data - берет из формы те данные которые у нас приходят {'name': 'Макс', 'email': 'staspv4@gmail.com', 'content': 'Не могу дозвониться'}
        subject = 'Message' # тема письма
        body = { # тело письма
            'name': form.cleaned_data['name'],
            'email': form.cleaned_data['email'],
            'content': form.cleaned_data['content']
        }
        message = '\n'.join(body.values()) # Само сообщение
        try:
            send_mail(subject, message, form.cleaned_data['email'], ['stas.perm000@mail.ru']) # попробуем отправить через данный метод 1 параметр subject - тема письма 2 - message сообщение, 3 from_email - от кого будет отправляться письмо, recipient_list - список, кому будет приходить данное письмо на какие адреса.
        except BadHeaderError:
            return HttpResponse('Найден не корректный заголовок')
        return redirect('index')
        # Отправка на почту это должны быть настройки почтового клиента.