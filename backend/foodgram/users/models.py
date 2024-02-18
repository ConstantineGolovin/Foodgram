from django.contrib.auth.models import AbstractUser
from django.db import models

from ..constants import MAX_LENGTH


class User(AbstractUser):
    """Модель кастомного юзера"""

    first_name = models.CharField(
        'Логин',
        max_length=MAX_LENGTH
    )
    last_name = models.CharField(
        'Фамилия',
        max_length=MAX_LENGTH
    )
    username = models.CharField(
        'Ник пользователя',
        max_length=MAX_LENGTH,
        unique=True
    )
    email = models.EmailField(
        'Email',
        max_length=MAX_LENGTH,
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


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author'],
                name='unique_user_author'
            )
        ]

    def __str__(self):
        return f'{self.author}{self.user}'
