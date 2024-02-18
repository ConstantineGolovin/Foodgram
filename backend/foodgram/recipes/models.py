from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from users.models import User
from recipes.constants import (MAX_LENGTH, MAX_LENGTH_COLOR_HEX,
                               MAX_LENGTH_MEASUREMENT_UNIT, MAX_LENGTH_TEXT,
                               MIN_VALUE, MAX_VALUE)


class Ingredient(models.Model):
    """Модель ингредиента"""

    name = models.CharField(
        'Ингредиент',
        max_length=MAX_LENGTH
    )
    measurement_unit = models.CharField(
        'Единицы измерения',
        max_length=MAX_LENGTH_MEASUREMENT_UNIT
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
        max_length=MAX_LENGTH
    )
    color = ColorField(
        verbose_name='HEX',
        unique=True,
        max_length=MAX_LENGTH_COLOR_HEX
    )
    slug = models.SlugField(
        'Слаг',
        unique=True
    )

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""

    name = models.CharField(
        'Название',
        max_length=MAX_LENGTH
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Тэги'
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Ингредиент',
        through='CountIngredientInRecipe'
    )
    text = models.TextField(
        'Описание',
        max_length=MAX_LENGTH_TEXT
    )
    cooking_time = models.PositiveIntegerField(
        'Время',
        validators=[MinValueValidator(
            MIN_VALUE, f'Время не может быть меньше {MIN_VALUE} мин'
        ), MaxValueValidator(
            MAX_VALUE, f'Время не может быть больше {MAX_VALUE} мин'
        )
        ]
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
    created = models.DateTimeField(
        'Дата',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-created',)

    def __str__(self):
        return self.name


class Favorite(models.Model):
    """Модель избранного"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'user'],
                name='unique_favorite'
            )
        ]

    def __str__(self):
        return f'{self.user}{self.recipe}'


class CountIngredientInRecipe(models.Model):
    """Количество ингредиентов в рецепте"""

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='countingredientinrecipe',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='countingredientinrecipe',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator(
            MIN_VALUE, f'Количество не может быть меньше {MIN_VALUE}'
        ), MaxValueValidator(
            MAX_VALUE, f'Количество не может быть больше{MAX_VALUE}'
        )
        ]
    )

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_recipe_ingredient'
            )
        ]

    def __str__(self):
        return f'{self.recipe}{self.ingredient}'


class ShoppingCart(models.Model):
    """Модель с корзины с покупками"""

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shoppingcart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]

    def __str__(self):
        return f'{self.user}{self.recipe}'
