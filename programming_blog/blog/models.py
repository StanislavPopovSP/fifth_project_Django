from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255) # обязательное для заполнения
    slug = models.SlugField(max_length=255, unique=True) # название транслитерации какой-то статьи, что-бы в адресной строке появлялось в место id если будем заходить на конкретную новость, либо запись, что бы в адресной строке прописывалось полностью название новости. Не может быть с одним и тем же названием.
    content = models.TextField(blank=True) # контент статьи
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True) # Y-год, m - месяц, d - день
    time_created = models.DateTimeField(auto_now_add=True) # дата создания какой-то записи
    time_update = models.DateTimeField(auto_now=True) # фиксация даты обновления, будет фиксироваться автоматически, в момент когда мы будем создать какую-то запись.
    # мы можем опубликовывать запись или создавать в той-же админке, а подготовить набор элементов и в нужный момент их публиковать.
    is_published = models.BooleanField(default=True) # может быть опубликована, может нет. По умолчанию опубликована.
    cat = models.ForeignKey('Category', on_delete=models.PROTECT) # категория. Так как класс ниже, имя класса указываем в кавычках. Запрещается удалять записи из первичной модели, если она используется во вторичной, выдает исключение.

    def __str__(self):
        return self.title

    class Meta: # Это доп-1 функционал кот-й мы можем дополнять к классу.
        verbose_name = 'Новость' # verbose_name перевели элементы, которые перечисляются в единственном числе. В единственном числе.
        verbose_name_plural = 'Новости' # Во множественном числе.
        ordering = ['-time_created'] # сортировка по времени


class Category(models.Model):
    name = models.CharField(max_length=100) # название категории
    slug = models.SlugField(max_length=200, unique=True)

    def __str__(self):
        return self.name

    class Meta: # Это доп-й функционал кот-й мы можем дополнять к классу.
        verbose_name = 'Категория' # verbose_name перевели элементы, которые перечисляются в единственном числе. В единственном числе.
        verbose_name_plural = 'Категории' # Во множественном числе.