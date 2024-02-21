# Generated by Django 4.2.4 on 2023-11-22 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_owners_api', '0010_car_booking_razorpay_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='car_booking',
            name='applied_coupon',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='car_booking',
            name='basic_price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='car_booking',
            name='coupon_discount_amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='car_booking',
            name='tax_amount',
            field=models.FloatField(default=0.0),
        ),
    ]
