from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        'Ингредиент',
        max_length=150
    )
    measurement_unit = models.CharField(
        'Вес',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name


class Tag(models.Model):
    """Модель Тэга"""

    name = models.CharField(
        'Тэг',
        max_length=50
    )
    slug = models.SlugField(
        'Слаг',
        max_length=50
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Follow(models.Model):
    """Модель подписок"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follower'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='follow'
    )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'author']
            )
        ]

    def __str__(self):
        return f'{self.author}{self.user}'
