from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from recipes.models import (Ingredient, Tag, Recipe,
                            Follow, Favorite, ShoppingCart,
                            CountIngredientInRecipe)
from users.models import User
from api.serializers import (IngredientSerializers,
                             TagSerializers,
                             RecipesSerializer,
                             UserSerializer,
                             FollowSerializers,
                             CreateNewRecipeSerializer,
                             FavoriteSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipesSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_recipe(self, user, model, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        model.objects.create(user=user, recipe=recipe)
        if model.objects.filter(user=user, recipe=recipe):
            return Response(
                {'errors': 'Этот рецепт уже был добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, pk, user, model):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепт уже был удалён!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=[IsAuthenticated]
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(Favorite, request.user, pk)

    @action(
            methods=['POST', 'DELETE'],
            detail=True,
            permission_classes=[IsAuthenticated]
    )
    def use_shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(ShoppingCart, request.user, pk)

    def download_shopping_cart(self, request):
        ingredients = CountIngredientInRecipe.objects.filter(
            recipe__shopping_cart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount'))
        shopping_cart = ''
        shopping_cart += ''.join([
            f'{ingredient["ingredient__name"]}'
            f'{ingredient["ingredient__measurement_unit"]}'
            f'{ingredient["amount"]}'
            for ingredient in ingredients
        ])
        response = HttpResponse(shopping_cart, content_type='text/plan')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_cart.txt')
        return response

    def get_serializer_class(self):
        if self.action in ('retrieve', 'list'):
            return RecipesSerializer
        return CreateNewRecipeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated]
    )
    def subscribes(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializers(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            sub = Follow.objects.cerate(user=user, author=author)
            sub.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            sub = get_object_or_404(
                Follow,
                user=user,
                author=author
            )
            sub.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def is_subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(follow__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializers(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
