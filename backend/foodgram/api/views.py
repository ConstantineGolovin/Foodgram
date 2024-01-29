from rest_framework import viewsets

from recipes.models import Ingredient, Tag
from api.serializers import IngredientSerializers, TagSerializers


class IngredientViewSet(viewsets.ReadOnlyModelViewSets):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers
