# Generated by Django 3.0.3 on 2020-10-27 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0031_auto_20201027_0122'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gps',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupID', models.CharField(max_length=100, unique=True)),
                ('group_name', models.CharField(max_length=100)),
            ],
        ),
    ]
