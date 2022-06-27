# Generated by Django 4.0.5 on 2022-06-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_alter_productreview_product_alter_productreview_user'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='productreview',
            constraint=models.UniqueConstraint(fields=('product_id', 'user_id'), name='unique_review_constraint'),
        ),
    ]
