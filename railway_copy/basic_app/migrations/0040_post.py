# Generated by Django 3.0.3 on 2020-11-11 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0039_auto_20201030_2316'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('groupID', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('post_content', models.TextField()),
            ],
        ),
    ]
