# Generated by Django 4.2.7 on 2023-11-30 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gt', '0007_remove_map_account_remove_map_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapBike',
            fields=[
                ('map_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('json_data', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='MapCar',
            fields=[
                ('map_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=100)),
                ('address', models.CharField(blank=True, max_length=200)),
                ('json_data', models.TextField(blank=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Map',
        ),
    ]
