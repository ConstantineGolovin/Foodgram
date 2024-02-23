import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Началась загрузка ингредиентов')
        with open('data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.load(file)
        for ingredient in ingredients:
            Ingredient.objects.bulk_create([
                Ingredient(name=ingredient['name']),
                Ingredient(measurement_unit=ingredient['measurement_unit'])],
                ignore_conflicts=True
            )

        print('Загрузка ингредиентов закончилась')
