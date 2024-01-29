from rest_framework import serializers

from recipes.models import Ingredient


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = '__all__'
