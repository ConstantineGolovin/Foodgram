from django.db import models

from users.models import User


class Ingredient(models.Model):
    """Модель ингредиента"""
    
    name = models.CharField(
        'Ингредиент',
        max_length=150
    )
    measurement_unit = models.CharField(
        'Вес',
        max_length=10
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient'
            )
        ]

    def __str__(self):
        return self.name