# Generated by Django 4.0.5 on 2022-09-08 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_order_total_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Payment',
        ),
    ]
