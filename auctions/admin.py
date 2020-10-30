from django.contrib import admin

from .models import User, Bid, Category, Listings, Comments

class ListingsAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "bid", "category", "url")

admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Listings, ListingsAdmin)
admin.site.register(Comments)
