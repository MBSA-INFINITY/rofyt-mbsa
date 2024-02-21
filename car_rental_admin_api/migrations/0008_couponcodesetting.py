# Generated by Django 4.2.4 on 2023-11-24 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('car_rental_admin_api', '0007_rename_extra_charges_vehiclerentepricesetting_extra_kms_charge_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CouponCodeSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('coupon_code', models.CharField(max_length=15)),
                ('coupon_discount', models.IntegerField()),
            ],
            options={
                'db_table': 'car_rental_coupon_code_setting',
            },
        ),
    ]