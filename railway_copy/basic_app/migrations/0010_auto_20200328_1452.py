# Generated by Django 3.0.3 on 2020-03-28 09:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0009_auto_20200328_1450'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nostoppingroute',
            name='train_no',
            field=models.IntegerField(),
        ),
    ]