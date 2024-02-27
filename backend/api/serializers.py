from django.contrib.auth import get_user_model
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers

from api.constants import MIN_INGR
from recipes.models import (CountIngredientInRecipe,
                            Favorite, Ingredient, Recipe,
                            ShoppingCart, Tag)
from recipes.constants import (MAX_VALUE_AMOUNT, MIN_VALUE_AMOUNT,
                               MIN_VALUE_TIME, MAX_VALUE_TIME)
from users.models import Follow


User = get_user_model()


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RecipeAndShoppingCartSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        if Favorite.objects.filter(
            user=data['user'],
            recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен'
            )
        return data

    def to_representation(self, instance):
        return RecipeAndShoppingCartSerializer(
            instance.recipe, context={
                'request': self.context.get('request')
            }
        ).data


class ShopingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShoppingCart
        fields = '__all__'

    def validate(self, data):
        if not self.context.get('request').method == 'POST':
            return data
        if Favorite.objects.filter(
            user=data['user'],
            recipe=data['recipe']
        ).exists():
            raise serializers.ValidationError(
                'Рецепт уже добавлен'
            )
        return data

    def to_representation(self, instance):
        return RecipeAndShoppingCartSerializer(
            instance.recipe, context={
                'request': self.context.get('request')
            }
        ).data


class UserSerializer(serializers.ModelSerializer):
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password', 'is_subscribed')

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or user is None:
            return False
        return Follow.objects.filter(
            author=obj.id,
            user=user
        ).exists()


class CreateUserSerializers(UserSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'username', 'email', 'password',)
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'password': {'required': True},
        }
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=('email', 'username'),
                message="Логин и email должны быть уникальными"
            )
        ]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class FollowSerializers(UserSerializer):
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count')
        read_only_fields = ('id', 'first_name', 'last_name',
                            'username', 'email', 'is_subscribed',
                            'recipes', 'recipes_count')

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_recipes(self, obj):
        recipe_limit = int(self.context['request'].GET.get('recipes_limit', 0))
        recipes = obj.recipes.all()
        recipes = recipes[:recipe_limit] if recipe_limit else recipes
        return ShortRecipeSerializer(recipes, many=True).data


class CreateFollowSerializer(serializers.ModelSerializer):

    class Meta:
        model = Follow
        fields = ('user', 'author')
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=Follow.objects.all(),
                fields=('author', 'user'),
                message='Невозможно подписаться, так как вы уже подписаны'
            )
        ]

    def validate(self, data):
        if data['user'] == data['author']:
            raise serializers.ValidationError(
                'Нельзя подписаться на себя'
            )
        return data

    def to_representation(self, instance):
        return FollowSerializers(
            instance.author, context={
                'request': self.context.get('request')
            }
        ).data


class CountIngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='ingredient.id')
    name = serializers.ReadOnlyField(source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = CountIngredientInRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientInRecipeSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    @staticmethod
    def validate_amount(value):
        if value < MIN_VALUE_AMOUNT:
            raise serializers.ValidationError(
                f'Количество ингредиента должно быть больше {MIN_VALUE_AMOUNT}'
            )
        if value > MAX_VALUE_AMOUNT:
            raise serializers.ValidationError(
                'Количество ингредиента не может '
                f'быть больше {MAX_VALUE_AMOUNT}'
            )
        return value

    class Meta:
        model = CountIngredientInRecipe
        fields = ('id', 'amount')


class RecipesSerializer(serializers.ModelSerializer):
    image = Base64ImageField()
    tags = TagSerializers(many=True)
    ingredients = CountIngredientInRecipeSerializer(
        many=True,
        source='countingredientinrecipe'
    )
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()
    author = UserSerializer(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

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


class CreateNewRecipeSerializer(serializers.ModelSerializer):
    ingredients = IngredientInRecipeSerializer(
        many=True,
        source='countingredientinrecipe'
    )
    image = Base64ImageField()
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )

    class Meta:
        model = Recipe
        fields = ('name', 'text', 'image', 'tags',
                  'ingredients', 'cooking_time')

    def choice_ingredient(self, recipe, ingredients):
        for ingredient in ingredients:
            CountIngredientInRecipe.objects.create(
                recipe=recipe,
                ingredient=ingredient['id'],
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        image_data = validated_data.pop('image')
        tag = validated_data.pop('tags')
        ingredients = validated_data.pop('countingredientinrecipe')
        recipe = Recipe.objects.create(image=image_data, **validated_data)
        recipe.tags.set(tag)
        self.choice_ingredient(ingredients=ingredients,
                               recipe=recipe)
        return recipe

    def validate_ingredient(self, ingredients):
        list_ingredients = []
        for ingredient in ingredients:
            if ingredient['id'] in list_ingredients:
                raise serializers.ValidationError(
                    'Ингредиент не может повторяться!'
                )
            if int(ingredient['amount']) <= MIN_INGR:
                raise serializers.ValidationError(
                    f'Количество ингредиента должно быть больше {MIN_INGR}'
                )
            list_ingredients.append(ingredient['id'])
        return ingredients

    def validate_cooking_time(self, cooking_time):
        if cooking_time < MIN_VALUE_TIME:
            raise serializers.ValidationError(
                f'Время не может быть меньше {MIN_VALUE_TIME}'
            )
        if cooking_time > MAX_VALUE_TIME:
            raise serializers.ValidationError(
                f'Время не может быть больше {MAX_VALUE_TIME}'
            )
        return cooking_time

    def validate_tags(self, tags):
        if not tags:
            raise serializers.ValidationError(
                {'tags': 'Нужно выбрать тэг'})
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise serializers.ValidationError(
                    {'tags': 'Тэги должны быть уникальными'})
            tags_list.append(tag)
        return tags

    def to_representation(self, instance):
        return RecipesSerializer(
            instance, context=self.context).data

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('countingredientinrecipe')
        instance.tags.clear()
        instance.ingredients.clear()
        instance.tags.set(tags)
        self.choice_ingredient(ingredients=ingredients, recipe=instance)
        return super().update(instance, validated_data)


class ShortRecipeSerializer(serializers.ModelSerializer):
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
