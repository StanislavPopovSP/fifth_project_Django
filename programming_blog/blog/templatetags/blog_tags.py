# Хотим сделать включающий тег, он позволяет дополнительно формировать свой собственный шаблон на основе
# некоторых данных и возвращать фрагмент html страницы.

from django import template # шаблоны django
from blog.models import * # из папки blog будем брать нашу модель

register = template.Library()
@register.inclusion_tag('blog/list_categories.html')  # нужно указать что это включающий тег
def show_categories(sort=None, cat_selected=0): # два принимаемых аргумента, они имеют значения по умолчанию.
    if not sort: # если нет сортировки
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats, 'cat_selected': cat_selected} # если cat_selected заменится на другое значение, то будет оно, или по умолчанию.