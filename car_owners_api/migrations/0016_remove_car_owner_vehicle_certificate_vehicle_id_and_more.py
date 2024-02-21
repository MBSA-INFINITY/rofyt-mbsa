# Generated by Django 4.2.4 on 2023-12-03 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('car_owners_api', '0015_car_owner_vehicle_is_approved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car_owner_vehicle_certificate',
            name='vehicle_id',
        ),
        migrations.RemoveField(
            model_name='car_owner_vehicle_image',
            name='vehicle_id',
        ),
        migrations.AddField(
            model_name='car_owner_vehicle_certificate',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='car_owners_api.car_owner_vehicle'),
        ),
        migrations.AddField(
            model_name='car_owner_vehicle_image',
            name='vehicle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='car_owners_api.car_owner_vehicle'),
        ),
    ]