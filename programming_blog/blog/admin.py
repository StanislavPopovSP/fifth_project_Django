from django.contrib import admin
from .models import *
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())  # В каком поле будет выводиться наш редактор

    class Meta:
        model = Blog
        fields = '__all__'


class BlogAdmin(admin.ModelAdmin):
    form = BlogAdminForm
    prepopulated_fields = {'slug': ('title',)}  # именованный параметр. {} - какое поле будет переводить другое поле. Ключ slug и что бы данные брал из поля title(передавать данные надо в виде кортежа.) Надо что бы slug переводил те данные кот-е есть в title.
    list_display = ('id', 'title', 'cat', 'time_created', 'photo', 'is_published')  # список отображаемых элементов, в него передаем кортеж и передаем какие поля хотим видеть. Чаще всего используется id номер самого элемента.
    list_display_links = ('id', 'title')  # Чтобы была ссылка на выбранные поля
    search_fields = ('title', 'content')  # поиск по полям
    list_editable = ('is_published',)  # для того что бы поле было кликабельным, для выбора не заходя по ссылке.
    list_filter = ('is_published', 'time_created')  # фильтр полей


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')
    search_fields = ('name',)


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
