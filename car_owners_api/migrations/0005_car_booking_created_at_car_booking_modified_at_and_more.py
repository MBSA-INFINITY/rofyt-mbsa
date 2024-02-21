# Generated by Django 4.2.4 on 2023-10-17 20:58

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('car_owners_api', '0004_car_booking_after_back_car_booking_after_front_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='car_booking',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='car_booking',
            name='modified_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='car_booking',
            name='booking_status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Canceled', 'Canceled'), ('Completed', 'Completed')], default='Pending', max_length=100),
        ),
    ]