from django.contrib.admin import ModelAdmin, register, site

from recipes.models import (Tag, Ingredient, Favorite,
                            Recipe, CountIngredientInRecipe,
                            ShoppingCart)

site.site_header = 'Администрирование Foodgram'
EMPTY_VALUE_DISPLAY = 'Значение не указано'


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('name', 'slug', 'color')


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)


@register(Favorite)
class FavoriteAdmin(ModelAdmin):
    list_display = ('user', 'recipe',)


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = ('name', 'id', 'author', 'favorite',)
    list_filter = ('author', 'name', 'tags',)

    def favorite(self, obj):
        return obj.favorites.count()


@register(CountIngredientInRecipe)
class CountIngredientInRecipeAdmin(ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('recipe', 'user',)
