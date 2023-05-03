from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *  # так как работа ведется с классами, то импортируем всё что есть в документе.

urlpatterns = [
    path('', BlogHome.as_view(), name='index'),  # as_views - привязать к маршруту. Т.е привязать текущий класс к текущему маршруту '' данного пути.
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),  # ставим slug для ceo оптимизации и вывода нашего slug. Тип данных slug и принимать post_slug. post_slug - поддерживает латиницу, ASCII символы, символы - и _ в post_slug - буквы и цифры могут располагаться, - и _ в принимаемый тип данных slug мы разрешаем чтобы попадал.
    path('category/<slug:cat_slug>/', BlogCategory.as_view(), name='category'),  # путь для какой-то категории
    path('addpage/', AddPage.as_view(), name='add_page'),  # путь для добавления статьи

    path('register/', RegisterUser.as_view(), name='register'),  # Путь для регистрации
    path('login/', LoginUser.as_view(), name='login'),  # Путь, что бы залогиниться
    path('logout/', auth_views.LogoutView.as_view(template_name='blog/logout.html'), name='logout'),  # auth_views.LogoutView - даст возможность разлогиниться
    path('contact/', ContactFormView.as_view(), name='contact'),  # для доступа к странице и форме контакт
]