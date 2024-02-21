# Generated by Django 4.2.4 on 2023-09-22 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0020_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='city',
            field=models.CharField(blank=True, max_length=74, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='house_or_building',
            field=models.CharField(blank=True, max_length=274, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='pincode',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='road_or_area',
            field=models.CharField(blank=True, max_length=274, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(blank=True, max_length=74, null=True),
        ),
    ]
