# Generated by Django 2.2.12 on 2020-04-23 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_auto_20200421_2230'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]
