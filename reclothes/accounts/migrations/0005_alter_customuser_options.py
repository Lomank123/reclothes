# Generated by Django 4.0.5 on 2022-09-30 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_remove_customuser_city_company_customuser_company'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customuser',
            options={'ordering': ['-id'], 'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
