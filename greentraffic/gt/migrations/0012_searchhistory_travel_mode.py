# Generated by Django 4.2.6 on 2023-12-11 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gt', '0011_searchhistory_end_location_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='searchhistory',
            name='travel_mode',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='トラベルモード'),
        ),
    ]
