# Generated by Django 3.0.3 on 2020-03-28 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0012_auto_20200328_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='nostoppingroute',
            name='seats',
            field=models.IntegerField(default=60),
            preserve_default=False,
        ),
    ]
