# Generated by Django 4.0.5 on 2022-07-05 09:28

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nais_storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seasonorder',
            name='quantity',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='количество'),
        ),
    ]