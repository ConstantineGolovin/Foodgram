import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Началась загрузка ингредиентов')
        with open('data/ingredients.json', encoding='utf-8') as file:
            ingredients = json.load(file)
        for ingredient in ingredients:
            if Ingredient.objects.filter(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit']
            ).exists():
                print(f'Ингредиент {ingredient["name"]} уже записан')
                continue
            Ingredient.objects.bulk_create(**ingredient)

        print('Загрузка ингредиентов закончилась')
