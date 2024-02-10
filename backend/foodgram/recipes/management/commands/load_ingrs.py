import json

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    def handle(self, *args, **options):
        print('Началась загрузка ингредиентов')
        ingredients = json.loads(
            (settings.BASE_DIR / 'data' / 'ingredients.json').read_text()
        )
        for ingredient in ingredients:
            if Ingredient.objects.filter(
                name=ingredient['name'],
                measurement_unit=ingredient['measurement_unit']
            ).exists():
                print(f'Ингредиент {ingredient["name"]} уже записан')
                continue
            Ingredient.objects.create(**ingredient)

        print('Загрузка ингредиентов закончилась')
