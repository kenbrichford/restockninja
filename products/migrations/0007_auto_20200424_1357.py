# Generated by Django 2.2.12 on 2020-04-24 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20200424_1249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upc',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
