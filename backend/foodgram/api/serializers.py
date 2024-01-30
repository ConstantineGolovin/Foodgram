from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Ingredient, Tag,
                            Follow, Recipe, CountIngredientInRecipe,
                            Favorite, ShoppingCart)
from users.models import User


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class FavoriteSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = '__all__'


class FollowSerializers(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    recipe = serializers.SerializerMethodField()
    recipe_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ('id', 'first_name', 'last_name',
                            'username', 'email', 'is_subscribed',
                            'recipe', 'recipe_count')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_authenticated or user is None:
            return False
        return Follow.objects.filter(
            user=obj,
            author=user
        ).exists()

    def get_recipe_count(obj):
        return obj.recipes.count()


class CountIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = CountIngredientInRecipe
        fields = '__all__'


class RecipesSerializers(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializers(blank=True)
    ingredients = CountIngredientInRecipeSerializer(
        many=True,
        source='countingredients'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('tags', 'author',
                            'is_favorited', 'is_is_shopping_cart')

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or user is None:
            return False
        return Favorite.objects.filter(
            user=user,
            recipe=obj
        ).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or user is None:
            return False
        return ShoppingCart.objects.filter(
            user=user,
            recipe=obj
        ).exists()


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()

    class Meta:
        model = CountIngredientInRecipe
        fields = '__all__'

    @staticmethod
    def validate_amount(count):
        if count > 1:
            return count
        raise serializers.ValidationError(
            'Количество не может быть меньше чем 1'
        )
