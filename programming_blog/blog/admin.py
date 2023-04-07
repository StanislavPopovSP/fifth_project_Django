from django.contrib import admin
from .models import *

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)} # именованный параметр. {} - какое поле будет переводить другое поле. Ключ slug и что бы данные брал из поля title(передавать данные надо в виде кортежа.) Надо что бы slug переводил те данные кот-е есть в title.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(Blog, BlogAdmin)
admin.site.register(Category, CategoryAdmin)
