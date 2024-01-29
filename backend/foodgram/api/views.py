from rest_framework import viewsets

from recipes.models import Ingredient
from api.serializers import IngredientSerializers


class IngredientViewSet(viewsets.ReadOnlyModelViewSets):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
