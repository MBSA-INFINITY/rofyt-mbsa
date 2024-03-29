# Generated by Django 4.2.4 on 2023-08-24 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0004_vehicle_vehiclemaker_vehiclemodel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabclass',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='cabclass',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='cabtype',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='cabtype',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]
