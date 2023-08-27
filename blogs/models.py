from django.db import models

from users.models import User


class Blog(models.Model):
    title = models.CharField(max_length=150, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Содержимое статьи')
    image = models.ImageField(verbose_name='Изображение', null=True, blank=True)
    views = models.IntegerField(default=0, verbose_name='Кол-во просмотров')
    date = models.DateTimeField(verbose_name='Дата публикации')

    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='автор')

    def __str__(self):
        return f'{self.title} {self.body} {self.image} {self.views} {self.date}'

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'