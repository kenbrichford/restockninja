# Generated by Django 2.2.12 on 2020-05-04 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0008_auto_20200503_2124'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]