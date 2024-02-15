from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet as DjoserUserViewSet
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from recipes.models import (Ingredient, Tag, Recipe,
                            Follow, Favorite, ShoppingCart,
                            CountIngredientInRecipe)
from api.serializers import (IngredientSerializers,
                             TagSerializers,
                             RecipesSerializer,
                             FollowSerializers,
                             CreateNewRecipeSerializer,
                             FavoriteSerializer)
from api.filters import IngredientFilter, RecipeFilter
from api.pagination import PagePagination
from api.permissions import AuthorOrReadOnly

User = get_user_model()


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PagePagination
    permission_classes = [AuthorOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def add_recipe(self, model, user, recipe_id):
        if model.objects.filter(user=user, recipe_id=recipe_id).exists():
            return Response(
                {'errors': 'Рецепт уже добавлен'},
                status=status.HTTP_400_BAD_REQUEST
            )
        recipe = get_object_or_404(Recipe, id=recipe_id)
        model.objects.create(user=user, recipe=recipe)
        serializer = FavoriteSerializer(recipe)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_recipe(self, model, user, recipe_id):
        obj = model.objects.filter(user=user, recipe_id=recipe_id)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'errors': 'Рецепт уже был удалён!'},
            status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def favorite(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(Favorite, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(Favorite, request.user, pk)

    @action(
        methods=['POST', 'DELETE'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def shopping_cart(self, request, pk):
        if request.method == 'POST':
            return self.add_recipe(ShoppingCart, request.user, pk)
        if request.method == 'DELETE':
            return self.delete_recipe(ShoppingCart, request.user, pk)

    @action(
        methods=('get',),
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def download_shopping_cart(self, request):
        ingredients = CountIngredientInRecipe.objects.filter(
            recipe__shoppingcart__user=request.user
        ).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(amount=Sum('amount')).order_by('ingredient__name')
        shopping_cart = 'Список покупок\n'
        shopping_cart += ''.join([
            f'{ingredient["ingredient__name"]}'
            f'{ingredient["ingredient__measurement_unit"]} '
            f'{ingredient["amount"]}\n'
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


class UserViewSet(DjoserUserViewSet):
    queryset = User.objects.all()
    pagination_class = PagePagination

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=[IsAuthenticated],
    )
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = FollowSerializers(
                author,
                data=request.data,
                context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            sub = Follow.objects.create(user=user, author=author)
            sub.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        sub = get_object_or_404(
            Follow,
            user=user,
            author=author
        )
        sub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        detail=True,
        permission_classes=[IsAuthenticated],
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

    @action(
        methods=['GET'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def subscriptions(self, request):
        queryset = User.objects.filter(follow__user=request.user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializers(
            pages,
            many=True,
            context={'request': request}
        )
        return self.get_paginated_response(serializer.data)
