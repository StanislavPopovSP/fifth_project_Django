from django import forms
from .models import *
from django.core.exceptions import ValidationError


class AddPostForm(forms.ModelForm):
    """Создание статьи"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана' # теперь будет писать категория не выбрана. Это обязательное поле, делаем что это поле обязательное для заполнения.

    class Meta:
        model = Blog
        fields = ['title', 'slug', 'content', 'photo', 'is_published', 'cat']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}), # у нас поле было точно такое же. 'class': 'form-input' - это будет имя класса. Через attrs передали дополнительные какие-то параметры.
            'slug': forms.TextInput(attrs={'class': 'form-input'}), # у нас поле было точно такое же. 'class': 'form-input' - это будет имя класса. Через attrs передали дополнительные какие-то параметры.
            'content': forms.Textarea(attrs={'cols':60, 'rows': 10, 'class': 'form-input'}) # attrs - это для атрибутов, атрибуты могут использоваться любые. 'cols': 60 - визуальное кол-во введенных символов, это как ширина пойдет, px и % можно установить только через css через класс.
        }