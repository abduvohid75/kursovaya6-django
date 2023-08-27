from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser, models.Model):
    username = None

    email = models.EmailField(unique=True, verbose_name='почта')

    avatar = models.ImageField(upload_to='users/avatars/', default='avatars/standart_avatar.png', verbose_name='аватар *Необязательное поле', null=True, blank=True)
    is_email_verified = models.BooleanField(default=False, verbose_name='статус верификации почты')
    is_blocked = models.BooleanField(default=False, verbose_name='Статус блокировки')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
