# Generated by Django 4.2.4 on 2023-12-05 08:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0026_alter_carownerphoneverify_user'),
        ('cab_booking_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer_Suppport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('phone', models.CharField(max_length=16)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('cutomer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.customer')),
            ],
            options={
                'db_table': 'cutomer_support',
            },
        ),
    ]
