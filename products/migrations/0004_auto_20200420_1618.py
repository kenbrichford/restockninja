# Generated by Django 2.2.12 on 2020-04-20 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_auto_20200420_1423'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Manufacturer',
            new_name='Brand',
        ),
        migrations.RenameField(
            model_name='product',
            old_name='manufacturer',
            new_name='brand',
        ),
    ]
