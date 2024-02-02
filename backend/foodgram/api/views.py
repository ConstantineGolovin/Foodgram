from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from recipes.models import Ingredient, Tag, Recipe, Follow
from users.models import User
from api.serializers import (IngredientSerializers,
                             TagSerializers,
                             RecipesSerializer,
                             UserSerializer,
                             FollowSerializers,
                             CreateNewRecipeSerializer)


class IngredientViewSet(viewsets.ReadOnlyModelViewSets):
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

    def delete_object(self, pk, user, model):
        obj = model.objects.filter(user=user, recipe__id=pk)
        if obj.exists():
            obj.delete()
            return Response(status=status.HTTP_201_CREATED)
        return Response(
            {'errors': 'Рецепт уже был удалён!'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
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
