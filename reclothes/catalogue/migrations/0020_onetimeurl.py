# Generated by Django 4.0.5 on 2022-10-01 04:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0019_remove_product_is_limited_remove_product_quantity'),
    ]

    operations = [
        migrations.CreateModel(
            name='OneTimeUrl',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url_token', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='Url token')),
                ('expired_at', models.DateTimeField(blank=True, null=True, verbose_name='Expiry date')),
                ('is_used', models.BooleanField(default=False, verbose_name='Already used')),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='one_time_urls', to='catalogue.productfile', verbose_name='File')),
            ],
            options={
                'verbose_name': 'One-Time Url',
                'verbose_name_plural': 'One-Time Urls',
                'ordering': ['-id'],
            },
        ),
    ]