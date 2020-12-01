from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f'{self.name}'

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    price = models.FloatField(default=0)
    category = models.ForeignKey(Category, blank=True, on_delete=models.CASCADE, related_name='Item_category')
    url = models.ImageField(blank=True, null=True, upload_to='images/')

    def __str__(self):
        return f'{self.id}: {self.title} bid on {self.price}'

class Bid(models.Model):
    user_id = models.ForeignKey(User, default='', on_delete=models.CASCADE, related_name='user_bid')
    auction_id = models.ForeignKey(Listings, default='', on_delete=models.CASCADE, related_name='auction_bid')
    amount = models.FloatField()

    def __str__(self):
        return f'£{self.amount}'

class Comments(models.Model):
    description = models.CharField(max_length=100)
    listing = models.ManyToManyField(Listings, blank=True, related_name='Item')

    def __str__(self):
        return f'Comments: {self.description}'

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    product = models.ForeignKey(Listings, on_delete=models.CASCADE, related_name='watchlist_item')

    def __str__(self):
        return f'{self.product}'
