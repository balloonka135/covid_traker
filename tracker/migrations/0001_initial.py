# Generated by Django 3.0.5 on 2020-04-26 12:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_url', models.URLField(blank=True)),
                ('profile_pic', models.ImageField(blank=True, upload_to='profile_pics')),
                ('occupation', models.CharField(blank=True, help_text='Enter your occupation (e.g. student)', max_length=100, verbose_name='Occupation type')),
                ('infection_status', models.CharField(blank=True, help_text='Enter your infection status (e.g. treated)', max_length=100, verbose_name='Infection status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
