# Generated by Django 4.0.5 on 2022-09-30 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0018_alter_activationkey_options_alter_category_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='is_limited',
        ),
        migrations.RemoveField(
            model_name='product',
            name='quantity',
        ),
    ]
