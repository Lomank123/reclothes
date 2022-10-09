# Generated by Django 4.0.5 on 2022-09-30 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0017_product_guide_alter_product_keys_limit'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activationkey',
            options={'ordering': ['-id'], 'verbose_name': 'Activation key', 'verbose_name_plural': 'Activation keys'},
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['-id'], 'verbose_name': 'Category', 'verbose_name_plural': 'Categories'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-id'], 'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
        migrations.AlterModelOptions(
            name='productattribute',
            options={'ordering': ['-id'], 'verbose_name': 'Product Attribute', 'verbose_name_plural': 'Product Attributes'},
        ),
        migrations.AlterModelOptions(
            name='productattributevalue',
            options={'ordering': ['-id'], 'verbose_name': 'Product Attribute Value', 'verbose_name_plural': 'Product Attribute Values'},
        ),
        migrations.AlterModelOptions(
            name='productimage',
            options={'ordering': ['-id'], 'verbose_name': 'Product Image', 'verbose_name_plural': 'Product Images'},
        ),
        migrations.AlterModelOptions(
            name='productreview',
            options={'ordering': ['-id'], 'verbose_name': 'Product Review', 'verbose_name_plural': 'Product Reviews'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'ordering': ['-id'], 'verbose_name': 'Product Type', 'verbose_name_plural': 'Product Types'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['-id'], 'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.RemoveField(
            model_name='tag',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='updated_at',
        ),
        migrations.AlterField(
            model_name='activationkey',
            name='key',
            field=models.CharField(help_text='Must be unique.', max_length=512, unique=True, verbose_name='Activation key'),
        ),
        migrations.AlterField(
            model_name='productattribute',
            name='name',
            field=models.CharField(help_text='Required and unique.', max_length=255, unique=True, verbose_name='Attribute name'),
        ),
    ]