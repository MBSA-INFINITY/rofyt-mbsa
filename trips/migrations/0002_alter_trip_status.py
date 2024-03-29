# Generated by Django 4.2.4 on 2023-08-24 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(blank=True, choices=[('ACCEPTED', 'ACCEPTED'), ('REJECTED', 'REJECTED'), ('BOOKED', 'BOOKED'), ('CANCELLED', 'CANCELLED'), ('ON_TRIP', 'ON_TRIP'), ('COMPLETED', 'COMPLETED')], max_length=74, null=True),
        ),
    ]
