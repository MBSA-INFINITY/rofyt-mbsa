# Generated by Django 4.2.4 on 2023-12-02 15:04

import cabs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0019_alter_vehiclemodel_cab_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclemodel',
            name='model_image',
            field=models.FileField(blank=True, null=True, upload_to=cabs.models.vehicle_model_directory_path),
        ),
    ]