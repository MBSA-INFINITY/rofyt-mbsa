# Generated by Django 4.2.4 on 2023-11-13 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_admin_api', '0005_remove_vehiclerentepricesetting_extra_charge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='fast_kms',
            field=models.IntegerField(default=0, verbose_name='set kms base on per hour'),
        ),
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='platform_charge',
            field=models.IntegerField(default=0, verbose_name='platform charge pasentage'),
        ),
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='second_kms',
            field=models.IntegerField(default=0, verbose_name='set kms base on per hour'),
        ),
        migrations.AlterField(
            model_name='vehiclerentepricesetting',
            name='third_kms',
            field=models.IntegerField(default=0, verbose_name='set kms base on per hour'),
        ),
    ]