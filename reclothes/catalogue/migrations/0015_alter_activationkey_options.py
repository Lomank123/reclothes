# Generated by Django 4.0.5 on 2022-09-17 06:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0014_alter_productfile_product'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activationkey',
            options={'ordering': ['-expired_at'], 'verbose_name': 'Activation key', 'verbose_name_plural': 'Activation keys'},
        ),
    ]
