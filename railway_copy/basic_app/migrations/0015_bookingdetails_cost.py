# Generated by Django 3.0.3 on 2020-03-28 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0014_nostoppingroute_price'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingdetails',
            name='cost',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]