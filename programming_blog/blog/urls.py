from django.urls import path
from .views import * # так как работа ведется с классами, то импортируем всё что есть в документе.

urlpatterns = [
    path('', BlogHome.as_view(), name='index'), # as_views - привязать к маршруту. Т.е привязать текущий класс к текущему маршруту '' данного пути.
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'), # ставим slug для ceo оптимизации и вывода нашего slug. Тип данных slug и принимать post_slug. post_slug - поддерживает латиницу, ASCII символы, символы - и _ в post_slug - буквы и цифры могут располагаться, - и _ в принимаемый тип данных slug мы разрешаем чтобы попадал.
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'), # путь для какой-то категории
    path('addpage/', AddPage.as_view(), name='add_page'), # путь для добавления статьи
]