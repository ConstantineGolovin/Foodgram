from colorfield.fields import ColorField
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from recipes.constants import (MAX_LENGTH, MAX_LENGTH_COLOR_HEX,
                               MAX_LENGTH_MEASUREMENT_UNIT, MAX_LENGTH_TEXT,
                               MIN_VALUE_AMOUNT, MAX_VALUE_AMOUNT,
                               MIN_VALUE_TIME, MAX_VALUE_TIME)
from users.models import User


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
    cooking_time = models.PositiveSmallIntegerField(
        'Время',
        validators=[MinValueValidator(
            MIN_VALUE_TIME, f'Время не может быть меньше {MIN_VALUE_TIME} мин'
        ), MaxValueValidator(
            MAX_VALUE_TIME, f'Время не может быть больше {MAX_VALUE_TIME} мин'
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


class FavoriteAndShoppingCartABS(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.user}{self.recipe}'


class Favorite(FavoriteAndShoppingCartABS):
    """Модель избранного"""

    class Meta(FavoriteAndShoppingCartABS.Meta):
        default_related_name = 'favorites'
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite'
            )
        ]


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
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator(
            MIN_VALUE_AMOUNT, 'Количество не может '
                              f'быть меньше {MIN_VALUE_AMOUNT}'
        ), MaxValueValidator(
            MAX_VALUE_AMOUNT, 'Количество не может '
                              f'быть больше{MAX_VALUE_AMOUNT}'
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


class ShoppingCart(FavoriteAndShoppingCartABS):
    """Модель с корзины с покупками"""

    class Meta(FavoriteAndShoppingCartABS.Meta):
        default_related_name = 'shoppingcart'
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shoppingcart'
            )
        ]
