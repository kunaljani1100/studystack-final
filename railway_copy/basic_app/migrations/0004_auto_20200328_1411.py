# Generated by Django 3.0.3 on 2020-03-28 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0003_auto_20200328_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='train',
            name='train_no',
            field=models.IntegerField(unique=True),
        ),
    ]
