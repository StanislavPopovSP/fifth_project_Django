from django.urls import path
from .views import * # так как работа ведется с классами, то импортируем всё что есть в документе.

urlpatterns = [
    path('', BlogHome.as_views(), name='index'), # as_views - привязать к маршруту. Т.е привязать текущий класс к текущему маршруту '' данного пути.
]