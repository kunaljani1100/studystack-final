# Generated by Django 3.0.3 on 2020-11-17 07:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0040_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupassociation',
            name='group_name',
            field=models.CharField(default='grp', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='group_name',
            field=models.CharField(default='grp', max_length=100),
            preserve_default=False,
        ),
    ]