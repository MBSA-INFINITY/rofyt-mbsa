# Generated by Django 4.2.4 on 2023-11-13 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_admin_api', '0003_rename_city_citysetting_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehiclerentepricesetting',
            name='extra_charges',
            field=models.IntegerField(default=0, verbose_name='Extra Charge for per kms'),
        ),
        migrations.AddField(
            model_name='vehiclerentepricesetting',
            name='extra_charge',
            field=models.IntegerField(default=0, verbose_name='Extra Charge for per kms'),
        ),
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='with_fuel_price',
            field=models.FloatField(default=0.0, verbose_name='with fuel vehicle rente price for per kms'),
        ),
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='without_fuel_price',
            field=models.FloatField(default=0.0, verbose_name='without fuel vehicle rente price for per kms'),
        ),
    ]
