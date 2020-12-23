# Generated by Django 3.0.8 on 2020-12-22 18:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0022_listings_creator'),
    ]

    operations = [
        migrations.CreateModel(
            name='Auction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('winner', models.CharField(blank=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('auction', models.ManyToManyField(blank=True, related_name='Item', to='auctions.Auction')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64)),
                ('description', models.CharField(max_length=300)),
                ('price', models.FloatField(default=0)),
                ('url', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('category', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='Item_category', to='auctions.Category')),
                ('creator', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='user_creator', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='listings',
            name='category',
        ),
        migrations.RemoveField(
            model_name='listings',
            name='creator',
        ),
        migrations.RenameField(
            model_name='bid',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='bid',
            name='auction_id',
        ),
        migrations.DeleteModel(
            name='Comments',
        ),
        migrations.AddField(
            model_name='auction',
            name='product',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='product_auction', to='auctions.Product'),
        ),
        migrations.AddField(
            model_name='bid',
            name='auction',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='auction_bid', to='auctions.Auction'),
        ),
        migrations.AlterField(
            model_name='watchlist',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='watchlist_item', to='auctions.Auction'),
        ),
        migrations.DeleteModel(
            name='Listings',
        ),
    ]
