from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name='Item_Category')
    url = models.ImageField(blank=True, null=True, upload_to='images/')
    date_posted = models.DateTimeField(auto_now_add=True, blank=True)
    creator = models.ForeignKey(User, default='', on_delete=models.CASCADE, related_name='User_Creator')

    def __str__(self):
        return f'{self.title}'

class Auction(models.Model):
    product = models.ForeignKey(Product, default='', on_delete=models.CASCADE, related_name='Product_Auction')
    active = models.BooleanField(default=True)
    winner = models.CharField(max_length=64, blank=True)

    def __str__(self):
        return f'{self.product}'

class Bid(models.Model):
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE, related_name='User_Bid')
    auction = models.ForeignKey(Auction, default='', on_delete=models.CASCADE, related_name='Auction_Bid')
    amount = models.FloatField()

    def __str__(self):
        return f'{self.auction.product} bid on {self.amount}'

class Comment(models.Model):
    description = models.CharField(max_length=100)
    auction = models.ForeignKey(Auction, default='', on_delete=models.CASCADE, related_name='Item')
    user = models.ForeignKey(User, default='', on_delete=models.CASCADE, related_name='Comment_Owner')
    time_sent = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comments: {self.description}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='User')
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name='Watchlist_Item')

    def __str__(self):
        return f'{self.auction}'
