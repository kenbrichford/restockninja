# Generated by Django 2.2.12 on 2020-05-03 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_remove_product_featured'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='total_alerts',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
