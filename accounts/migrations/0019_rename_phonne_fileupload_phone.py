# Generated by Django 4.2.4 on 2023-09-05 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0018_fileupload_phonne_alter_fileupload_file'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fileupload',
            old_name='phonne',
            new_name='phone',
        ),
    ]
