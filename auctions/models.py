from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    amount = models.FloatField()

    def __str__(self):
        return f'£{self.amount}'

class Listings(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=300)
    bid = models.ForeignKey(Bid, on_delete=models.CASCADE, related_name='Item_bid')
    url = models.ImageField(blank=True)

    def __str__(self):
        return f'{self.id}: {self.title} bid on {self.bid}'

class Comments(models.Model):
    description = models.CharField(max_length=100)
    listing = models.ManyToManyField(Listings, blank=True, related_name='Item')

    def __str__(self):
        return f'Comments: {self.description}'
