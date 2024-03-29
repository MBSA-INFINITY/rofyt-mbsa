# Generated by Django 4.2.4 on 2023-10-10 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0024_alter_carownerphoneverify_user_and_more'),
        ('car_owners_api', '0002_car_owner_vehicle_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='car_owner_vehicle',
            name='vehicle_type_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.CreateModel(
            name='Car_Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pick_up_locations', models.CharField(blank=True, max_length=100, null=True)),
                ('drop_off_locations', models.CharField(blank=True, max_length=100, null=True)),
                ('pick_up_data_time', models.DateTimeField()),
                ('drop_up_date_time', models.DateTimeField()),
                ('booking_status', models.CharField(choices=[('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Canceled', 'Canceled')], default='Pending', max_length=100)),
                ('payment_status', models.CharField(choices=[('PAID', 'Paid'), ('PENDING', 'Pending'), ('FAILED', 'Failed'), ('REFUNDED', 'Refunded')], max_length=10)),
                ('payment_price', models.FloatField()),
                ('car_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_car_owner', to='accounts.carowner')),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings_as_customer', to='accounts.customer')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='car_owners_api.car_owner_vehicle')),
            ],
            options={
                'db_table': 'car_booking',
            },
        ),
    ]
