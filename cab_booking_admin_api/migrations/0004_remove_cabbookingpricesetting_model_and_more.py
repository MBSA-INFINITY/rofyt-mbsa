# Generated by Django 4.2.4 on 2023-11-26 12:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0016_alter_vehiclemodel_model_image'),
        ('cab_booking_admin_api', '0003_cabbookingcouponcodesetting'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cabbookingpricesetting',
            name='model',
        ),
        migrations.AddField(
            model_name='cabbookingpricesetting',
            name='cab_class',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.PROTECT, to='cabs.cabclass'),
        ),
    ]
