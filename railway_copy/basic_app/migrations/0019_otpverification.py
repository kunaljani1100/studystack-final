# Generated by Django 3.0.3 on 2020-08-08 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0018_auto_20200328_2244'),
    ]

    operations = [
        migrations.CreateModel(
            name='OTPVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emailID', models.CharField(max_length=100, unique=True)),
                ('otp', models.CharField(max_length=4)),
            ],
        ),
    ]
