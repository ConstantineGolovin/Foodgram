from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Модель кастомного юзера"""

    first_name = models.CharField(
        'Логин',
        max_length=150
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=150
    )
    username = models.CharField(
        'Ник пользователя',
        max_length=150,
        unique=True
    )
    email = models.EmailField(
        'Email',
        max_length=150,
        unique=True
    )
    is_subscribed = models.BooleanField(
        'Подписка',
        default=False
    )

    REQUIRED_FIELDS = ['first_name', 'last_name', 'username']
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        constraints = [
            models.UniqueConstraint(
                fields=['username', 'email'],
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
