# Generated by Django 4.1.2 on 2022-10-17 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_file_first_name_file_last_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='email',
            field=models.EmailField(default='', max_length=254),
        ),
    ]