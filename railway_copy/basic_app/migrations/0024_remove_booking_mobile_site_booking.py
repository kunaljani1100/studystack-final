# Generated by Django 3.0.3 on 2020-10-17 21:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0023_booking'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='mobile_site_booking',
        ),
    ]