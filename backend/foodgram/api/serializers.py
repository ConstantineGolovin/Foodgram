from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField

from recipes.models import (Ingredient, Tag,
                            Follow, Recipe, CountIngredientInRecipe)
from users.models import User


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
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
        if user.is_authenticated:
            return Follow.objects.filter(
                user=obj,
                author=user
            ).exists()
        return False

    def get_recipe_count(obj):
        return obj.recipes.count()


class RecipesSerializers(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializers(blank=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('tags', 'author')


class CountIngredientInRecipe(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = CountIngredientInRecipe
        fields = '__all__'
