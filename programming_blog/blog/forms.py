from django import forms
from .models import *
from django.core.exceptions import ValidationError  # проверка на валидацию своих каких то элементов.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    """Создание статьи"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'  # теперь будет писать категория не выбрана. Это обязательное поле, делаем что это поле обязательное для заполнения.

    def clean_title(self):
        """Проверка на валидацию, ограничение кол-ва символов"""
        title = self.cleaned_data['title']  # cleaned_data - это будет какой-то пользовательский валидатор. Наследуемся из модели, к нему добавляем доп проверку. К cleaned_data добавляем дополнительную проверку.
        # Допустим если при заполнении случайно отдельно написали название статьи и контента и в названии написали очень большой заголвок, больше 200 символов, что бы нам показвало ошибку, что длина превышает больше какого-то кол-ва символов.
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title  # если не попали в raise возвращаем title

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),  # у нас поле было точно такое же. 'class': 'form-input' - это будет имя класса. Через attrs передали дополнительные какие-то параметры.
            'slug': forms.TextInput(attrs={'class': 'form-input'}),  # у нас поле было точно такое же. 'class': 'form-input' - это будет имя класса. Через attrs передали дополнительные какие-то параметры.
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-input'})  # attrs - это для атрибутов, атрибуты могут использоваться любые. 'cols': 60 - визуальное кол-во введенных символов, это как ширина пойдет, px и % можно установить только через css через класс.
        }


class RegisterUserForm(UserCreationForm):
    """Берем все свойства и методы UserCreationForm,
     переопределяем свойства родительские и добавим свои поля.
     Форма для регистрации пользователя."""
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input'})) # EmailField - будет добавлять проверку на валидацию поля
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        """Для отображения правильного порядка который нам нужен"""
        model = User # В данную модель будем данные сохранять
        fields = ['username', 'email', 'password1', 'password2']

class ContactForm(forms.Form): # Наследуемся от стандартной формы Джанго, для создания своей формы.
    """Своя форма обратной связи"""
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Сообщения', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()
