# Generated by Django 2.1.7 on 2019-03-31 22:46

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('load', '0002_auto_20190320_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='load',
            name='pickup_date',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
