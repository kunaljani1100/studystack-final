# Generated by Django 3.0.3 on 2020-03-28 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0011_bookingdetails'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='train_no',
            field=models.CharField(max_length=5, unique=True),
        ),
    ]
