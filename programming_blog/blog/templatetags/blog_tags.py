# Хотим сделать включающий тег,
# он позволяет дополнительно формировать свой собственный шаблон на основе
# некоторых данных и возвращать фрагмент html страницы.

from django import template  # шаблоны django
from blog.models import *  # из папки blog будем брать нашу модель

register = template.Library()


@register.inclusion_tag('blog/list_categories.html')  # нужно указать что это включающий тег
def show_categories(sort=None):  # два принимаемых аргумента, они имеют значения по умолчанию. Их создали сами.
    if not sort:  # если нет сортировки
        cats = Category.objects.all()
    else:
        cats = Category.objects.order_by(sort)
    return {'cats': cats}  # если cat_selected заменится на другое значение, то будет оно, или по умолчанию.



## Как пример других забросов
# @register.simple_tag() - забирает какую-то информацию от куда либо, он ее просто передает context в шаблон, где мы вызовем этот тег, и он вернет эту информацию.
# def get_catigories():
#     """Вывод всех категорий"""
#     return Category.objects.all()


# @register.inclusion_tag('movies/tags/last_movie.html') - рендерит шаблон, где мы вызовим этот temlate тег он вернет отрендариный html
#     def get_last_movies(count=5):
#         movie = Movie.objects.order_by('id')[:count]
#         return {'last_movies': movie}
