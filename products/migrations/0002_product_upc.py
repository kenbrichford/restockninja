# Generated by Django 2.2.12 on 2020-04-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='upc',
            field=models.CharField(default=1, max_length=12),
            preserve_default=False,
        ),
    ]
