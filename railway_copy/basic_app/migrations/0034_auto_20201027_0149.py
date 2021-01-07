# Generated by Django 3.0.3 on 2020-10-27 08:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0033_auto_20201027_0137'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booking',
            old_name='booking_created',
            new_name='groupID',
        ),
        migrations.RenameField(
            model_name='booking',
            old_name='car_cancellation',
            new_name='group_name',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='emailID',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='from_area_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='from_city_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='from_lat',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='from_long',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='mobile_booking',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='online_booking',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='package_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='to_area_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='to_city_id',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='to_date',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='to_lat',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='to_long',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='travel_type',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='vehicle_id',
        ),
    ]
