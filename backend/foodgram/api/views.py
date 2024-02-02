from rest_framework import viewsets, status
from rest_framework.response import Response

from recipes.models import Ingredient, Tag, Recipe
from api.serializers import (IngredientSerializers,
                             TagSerializers,
                             RecipesSerializer)


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
