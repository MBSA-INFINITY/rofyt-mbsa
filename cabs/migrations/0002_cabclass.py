# Generated by Django 4.2.4 on 2023-08-18 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cabs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CabClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cab_type', models.CharField(max_length=74)),
            ],
        ),
    ]
