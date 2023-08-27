from django.db import models

from users.models import User

class Client(models.Model):
    avatar = models.ImageField(verbose_name='аватар', default='avatars\standart_avatar.png', null=True)

    name = models.CharField(max_length=100, verbose_name='имя')
    email = models.EmailField(verbose_name='почта')
    comment = models.TextField(verbose_name='комментарий', null=True, blank=True)

    mail = models.ForeignKey('Mails', on_delete=models.CASCADE, null=True, blank=True, verbose_name='рассылки')

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'{self.name} {self.email} {self.author}'
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

class Mails(models.Model):
    users = models.ManyToManyField(Client, verbose_name='клиент')
    theme = models.CharField(max_length=255, verbose_name='тема', null=True)
    body = models.TextField(verbose_name='текст', null=True)
    status = models.BooleanField(default=False, verbose_name='статус')

    author = models.ForeignKey(User, verbose_name='Автор', on_delete=models.CASCADE)

    scheduled = models.DateTimeField(null=True, blank=True, verbose_name='запланированное время запуска')
    periodic = models.IntegerField(null=True, blank=True, verbose_name='периодичное время запуска(мин.)')
    dynamic_periodic = models.IntegerField(null=True, blank=True, verbose_name='периодичное время запуска(мин.)')

    end = models.DateTimeField(null=True, blank=True, verbose_name='время окончания рассылки')

    logs = models.ForeignKey('Logs', on_delete=models.CASCADE, verbose_name='логи', null=True, blank=True)


    def __str__(self):
        return f'{self.users} {self.theme} {self.body} {self.status} {self.scheduled} {self.periodic} {self.logs}'

    class Meta:
        verbose_name = 'рассылка'
        verbose_name_plural = 'рассылки'

class Logs(models.Model):
    last_time = models.DateTimeField(verbose_name='Время последней попытки', null=True, blank=True)
    status = models.BooleanField(verbose_name='Статус попытки', null=True, blank=True)
    response = models.CharField(max_length=300, verbose_name='Ответ сервера', null=True, blank=True)

    def __str__(self):
        return f'{self.last_time} {self.status} {self.response}'

    class Meta:
        verbose_name = 'логи'
        verbose_name_plural = 'логи'