# Generated by Django 3.1.3 on 2020-11-29 06:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0042_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupassociation',
            name='isAdmin',
            field=models.CharField(default='false', max_length=100),
            preserve_default=False,
        ),
    ]
