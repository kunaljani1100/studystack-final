# Generated by Django 3.0.3 on 2020-03-28 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0004_auto_20200328_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Station',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('station_code', models.CharField(max_length=3, unique=True)),
                ('station_name', models.CharField(max_length=50)),
            ],
        ),
    ]
