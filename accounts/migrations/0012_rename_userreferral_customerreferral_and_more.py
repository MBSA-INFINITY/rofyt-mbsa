# Generated by Django 4.2.4 on 2023-08-24 04:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_user_type'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserReferral',
            new_name='CustomerReferral',
        ),
        migrations.AlterField(
            model_name='customerreferral',
            name='referred',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='referrers', to='accounts.customer'),
        ),
        migrations.AlterField(
            model_name='customerreferral',
            name='referrer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='referreds', to='accounts.customer'),
        ),
    ]
