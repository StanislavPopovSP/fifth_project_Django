from django.shortcuts import render
from django.views.generic import ListView  # он за нас сделает большую работу, не надо будет указывать много элементов одновременно.
from .models import *


# если работаем с классом, то без модели он работать не может
class BlogHome(ListView):
    model = Blog
    template_name = 'blog/index.html' # куда будет выводиться HTML страница. template_name - как свойства в классе, они имеют определенное значение, что мы в них должны поместить.
    context_object_name = 'post' # Имя объекта внутри шаблона. Специальная переменная которая будет выводить код в html шаблон.