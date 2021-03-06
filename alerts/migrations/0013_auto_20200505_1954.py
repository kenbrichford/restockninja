# Generated by Django 2.2.12 on 2020-05-05 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alerts', '0012_alert_email_frequency'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alert',
            name='email_frequency',
            field=models.PositiveIntegerField(choices=[(604800, 'Weekly'), (86400, 'Daily'), (43200, 'Two per day'), (28800, 'Three per day'), (3600, 'Hourly'), (0, 'All updates')], default=86400),
        ),
    ]
