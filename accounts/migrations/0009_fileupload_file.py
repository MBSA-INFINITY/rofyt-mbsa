# Generated by Django 4.2.4 on 2023-08-23 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_fileupload'),
    ]

    operations = [
        migrations.AddField(
            model_name='fileupload',
            name='file',
            field=models.FileField(default=1, upload_to='upload/%Y/%m/%d'),
            preserve_default=False,
        ),
    ]
