# Generated by Django 3.0.3 on 2020-10-17 21:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0022_auto_20200813_2310'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailID', models.CharField(max_length=100, unique=True)),
                ('vehicle_id', models.CharField(max_length=100, unique=True)),
                ('package_id', models.CharField(max_length=100, unique=True)),
                ('travel_type', models.CharField(max_length=100, unique=True)),
                ('from_area_id', models.CharField(max_length=100, unique=True)),
                ('to_area_id', models.CharField(max_length=100, unique=True)),
                ('from_city_id', models.CharField(max_length=100, unique=True)),
                ('to_city_id', models.CharField(max_length=100, unique=True)),
                ('from_date', models.CharField(max_length=100, unique=True)),
                ('to_date', models.CharField(max_length=100, unique=True)),
                ('online_booking', models.CharField(max_length=100, unique=True)),
                ('mobile_booking', models.CharField(max_length=100, unique=True)),
                ('mobile_site_booking', models.CharField(max_length=100, unique=True)),
                ('booking_created', models.CharField(max_length=100, unique=True)),
                ('from_lat', models.CharField(max_length=100, unique=True)),
                ('from_long', models.CharField(max_length=100, unique=True)),
                ('to_lat', models.CharField(max_length=100, unique=True)),
                ('to_long', models.CharField(max_length=100, unique=True)),
                ('car_cancellation', models.CharField(max_length=100, unique=True)),
            ],
        ),
    ]
