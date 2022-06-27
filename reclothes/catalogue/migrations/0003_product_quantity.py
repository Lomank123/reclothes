# Generated by Django 4.0.5 on 2022-06-25 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0002_productattributevalue_unique_value_constraint'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='quantity',
            field=models.IntegerField(default=0, help_text='How many products have left', verbose_name='Quantity'),
        ),
    ]