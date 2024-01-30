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
                fields=['user', 'author']
            )
        ]

    def __str__(self):
        return f'{self.author}{self.user}'


class Recipe(models.Model):
    """Модель рецепта"""

    name = models.CharField(
        'Название',
        max_length=150
    )
    tags = models.ForeignKey(
        Tag,
        related_name='recipes',
        verbose_name='Тэг'
    )
    ingredients = models.ForeignKey(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент'
    )
    text = models.TextField(
        'Описание',
        max_length=1000
    )
    time = models.PositiveIntegerField(
        'Время'
    )
    image = models.ImageField(
        'Фото',
        upload_to='recipes/',
        blank=True
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return self.name
