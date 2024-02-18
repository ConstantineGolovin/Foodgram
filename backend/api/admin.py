from django.contrib.admin import ModelAdmin, TabularInline, register, site
from django.utils.safestring import mark_safe

from recipes.models import (Tag, Ingredient, Favorite,
                            Recipe, ShoppingCart)

site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


class IngredientInLine(TabularInline):
    model = Recipe.ingredients.through
    extra = 2
    min_num = 1


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color',)
    empty_value_display = EMPTY_VALUE_DISPLAY
    search_fields = ('name', 'color')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'author', 'get_image',
                    'get_ingredients', 'get_count_favourites')
    list_filter = ('author__username', 'name', 'tags',)
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    raw_id_fields = ('author',)
    search_fields = ('name', 'author__username', 'tags',)
    inlines = (IngredientInLine,)
    empty_valuse_display = EMPTY_VALUE_DISPLAY

    def get_ingredients(self, obj):
        return ', '.join(
            ingredient.ingredient.name
            for ingredient in obj.countingredientinrecipe.all()
        )

    def get_count_favourites(self, obj):
        return obj.favorites.count()

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" height="30"')

    get_image.short_description = 'Изображение'
    get_count_favourites.short_description = 'Добавили в избранное'
    get_ingredients.short_description = 'Ингредиенты'


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user',)
