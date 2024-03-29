# Generated by Django 4.2.4 on 2023-08-24 04:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_rename_userreferral_customerreferral_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PhoneVerify',
            new_name='CustomerPhoneVerify',
        ),
        migrations.AlterField(
            model_name='customerphoneverify',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='accounts.customer'),
        ),
        migrations.CreateModel(
            name='DriverPhoneVerify',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.PositiveIntegerField(blank=True, default=1, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='accounts.driver')),
            ],
        ),
    ]
