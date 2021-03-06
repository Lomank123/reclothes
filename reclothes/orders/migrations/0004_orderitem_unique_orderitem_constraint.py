# Generated by Django 4.0.5 on 2022-06-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_alter_order_address_alter_order_user_and_more'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='orderitem',
            constraint=models.UniqueConstraint(fields=('order_id', 'cart_item_id'), name='unique_orderitem_constraint'),
        ),
    ]
