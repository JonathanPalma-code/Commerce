# Generated by Django 3.0.8 on 2020-12-01 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20201201_1925'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listings',
            name='bid',
        ),
        migrations.AddField(
            model_name='listings',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
