# Generated by Django 3.0.3 on 2020-03-28 09:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic_app', '0005_station'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoStoppingRoute',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route_id', models.IntegerField(unique=True)),
                ('station1_code', models.CharField(max_length=3, unique=True)),
                ('station2_code', models.CharField(max_length=3, unique=True)),
                ('train_no', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='basic_app.Train')),
            ],
        ),
    ]