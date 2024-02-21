# Generated by Django 4.2.4 on 2023-08-28 17:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_customerreferral_updated_at_fileupload_updated_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarOwner',
            fields=[
            ],
            options={
                'proxy': True,
                'indexes': [],
                'constraints': [],
            },
            bases=('accounts.user',),
        ),
        migrations.AddField(
            model_name='user',
            name='is_carowner',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='driver_duty',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('DRIVER', 'driver'), ('CUSTOMER', 'customer'), ('CAROWNER', 'carowner')], default='CUSTOMER', max_length=11),
        ),
        migrations.CreateModel(
            name='CarOwnerPhoneVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='accounts.driver')),
            ],
        ),
    ]