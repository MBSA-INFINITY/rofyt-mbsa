# Generated by Django 4.2.4 on 2023-08-24 06:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_user_license_upload_back_user_myride_insurance_and_more'),
        ('cabs', '0003_cab_created_at_cab_is_active_cab_last_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('number_plate', models.CharField(max_length=74, unique=True)),
                ('insurance_certiifcate_1', models.TextField(blank=True, null=True)),
                ('last_location', models.CharField(blank=True, max_length=174, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleMaker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('maker', models.CharField(max_length=74)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now=True)),
                ('model', models.CharField(max_length=74)),
                ('maker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cabs.vehiclemaker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='cabtype',
            name='cab_class',
        ),
        migrations.AddField(
            model_name='cabclass',
            name='cab_class',
            field=models.CharField(default=1, max_length=74),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='cabclass',
            name='cab_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='cabs.cabtype'),
        ),
        migrations.DeleteModel(
            name='Cab',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='cab_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to='cabs.cabclass'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='cab_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to='cabs.cabtype'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='driver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to='accounts.driver'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='maker',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to='cabs.vehiclemaker'),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='vehicles', to='cabs.vehiclemodel'),
        ),
    ]
