# Generated by Django 4.2.4 on 2023-12-01 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_admin_api', '0008_couponcodesetting'),
    ]

    operations = [
        migrations.AddField(
            model_name='citysetting',
            name='city_image',
            field=models.TextField(default='https://www.shutterstock.com/image-vector/indian-city-icon-bangalorevidhan-soudha-karnataka-1455972629'),
        ),
    ]
