from django.contrib import admin

from .models import User, Bid, Category, Product, Auction, Comment, Watchlist

class ProductAdmin(admin.ModelAdmin):
  list_display = ("id", "title", "price", "category", "date_posted", "creator")

class AuctionAdmin(admin.ModelAdmin):
  list_display = ("id", "product", "winner", "active" )

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Auction, AuctionAdmin)
admin.site.register(Comment)
admin.site.register(Watchlist)
