# Generated by Django 4.2.4 on 2023-11-14 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0006_driverpricingratio'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='order_id',
            field=models.TextField(blank=True, max_length=74, null=True),
        ),
    ]