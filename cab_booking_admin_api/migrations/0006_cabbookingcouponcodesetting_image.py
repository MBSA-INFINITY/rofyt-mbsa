# Generated by Django 4.2.4 on 2023-11-30 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cab_booking_admin_api', '0005_cabbookingcouponcodesetting_expire_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='cabbookingcouponcodesetting',
            name='image',
            field=models.TextField(default='https://jlp108-my-ride.s3.amazonaws.com/media/myride/8900044488/png-clipart-city-car-sports-car-computer-icons-vehicle-city-silhouette_BFKXiKM.png'),
        ),
    ]
