# Generated by Django 2.1.1 on 2020-05-10 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='profile_pic',
        ),
    ]