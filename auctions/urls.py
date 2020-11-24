from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("add", views.add, name="add"),
    path("auction/<int:auction_id>", views.auction, name="auction"),
    path("watchlist/<int:user_id>", views.watchlist, name="watchlist")
]
