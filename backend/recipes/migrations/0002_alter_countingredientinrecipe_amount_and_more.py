# Generated by Django 4.0.4 on 2024-02-20 09:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='countingredientinrecipe',
            name='amount',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество не может быть меньше 1'), django.core.validators.MaxValueValidator(250, 'Количество не может быть больше250')], verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='cooking_time',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время не может быть меньше 1 мин'), django.core.validators.MaxValueValidator(250, 'Время не может быть больше 250 мин')], verbose_name='Время'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.CharField(max_length=150, verbose_name='Тэг'),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
