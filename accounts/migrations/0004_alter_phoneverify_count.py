# Generated by Django 4.2.4 on 2023-08-18 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_phoneverify'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phoneverify',
            name='count',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
    ]