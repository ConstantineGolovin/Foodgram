# Generated by Django 4.0.4 on 2024-02-22 18:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_favorite_options_alter_shoppingcart_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countingredientinrecipe',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество не может быть меньше 1'), django.core.validators.MaxValueValidator(1000, 'Количество не может быть больше1000')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время не может быть меньше 1 мин'), django.core.validators.MaxValueValidator(1440, 'Время не может быть больше 1440 мин')], verbose_name='Время'),
        ),
        migrations.AddConstraint(
            model_name='favorite',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite'),
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shoppingcart'),
        ),
    ]