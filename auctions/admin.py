from django.contrib import admin

from .models import User, Bid, Category, Listings, Comments, Watchlist

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "price", "category", "url")

class BidAdmin(admin.ModelAdmin):
    bid_display = ("id", "user_id", "auction_id", "amount")

admin.site.register(User)
admin.site.register(Bid, BidAdmin)
admin.site.register(Category)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Comments)
admin.site.register(Watchlist)
