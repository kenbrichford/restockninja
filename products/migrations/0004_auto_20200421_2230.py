# Generated by Django 2.2.12 on 2020-04-21 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_product_variants'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='variants',
            field=models.ManyToManyField(related_name='_product_variants_+', to='products.Product'),
        ),
    ]