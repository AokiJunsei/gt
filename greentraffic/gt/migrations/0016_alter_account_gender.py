# Generated by Django 4.2.7 on 2024-01-30 02:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gt', '0015_searchhistory_end_spot_label_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='gender',
            field=models.CharField(blank=True, choices=[('M', '男'), ('F', '女'), ('O', 'その他')], max_length=100),
        ),
    ]