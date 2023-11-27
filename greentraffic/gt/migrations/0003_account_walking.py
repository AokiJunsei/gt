# Generated by Django 4.2.6 on 2023-11-21 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gt', '0002_account_address_1_account_address_2_account_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='walking',
            field=models.CharField(blank=True, choices=[('Fast', 'はやい'), ('Normal', 'ふつう'), ('Slow', 'おそい')], max_length=100),
        ),
    ]
