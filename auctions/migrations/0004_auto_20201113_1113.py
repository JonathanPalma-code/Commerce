# Generated by Django 3.0.8 on 2020-11-13 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_auto_20201030_1414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listings',
            name='url',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]