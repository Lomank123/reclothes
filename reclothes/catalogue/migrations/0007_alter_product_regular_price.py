# Generated by Django 4.0.5 on 2022-06-29 14:14

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0006_alter_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='regular_price',
            field=models.DecimalField(decimal_places=2, help_text='Maximum 9999.99', max_digits=6, validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='Regular price'),
        ),
    ]
