from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import AddAuction, AddBid
from .models import User, Bid, Listings, Comments, Category, Watchlist

class ValueTooSmallError(Exception):
    pass

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def index(request):
    return render(request, "auctions/index.html",{
        'listings': Listings.objects.all(),
        'bids': Bid.objects.all()
    })

@login_required
def add(request):
    if request.method == 'POST':
        form = AddAuction(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            url = form.cleaned_data['url']
            listing = Listings.objects.create(title=title, description=description, price=price, category=category, url=url)
            bid = Bid.objects.create(amount=listing.price, auction_id=listing, user_id=request.user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/add', {
                'add_auction_form': form
            })
    return render(request, 'auctions/add.html', {
        'add_auction_form': AddAuction()
    })

def auction(request, auction_id):
    auction = Listings.objects.get(pk=auction_id)
    in_watch = None
    add_bid = auction.price
    
    if request.user.is_authenticated:
        in_watch = Watchlist.objects.filter(user=request.user, product=auction)
        add_bid = AddBid()

        if request.method == 'POST' and 'watchlist_btn' in request.POST:
            if in_watch:
                in_watch.delete()
                return HttpResponseRedirect(reverse('index'))
            else:
                add_wathlist = Watchlist.objects.create(user=request.user, product=auction)
                return HttpResponseRedirect(reverse('watchlist', args=[request.user.id]))
        
        if request.method == 'POST' and 'bid_btn' in request.POST:
            form = AddBid(request.POST)
            if form.is_valid():
                try: 
                    amount = form.cleaned_data['amount']
                    if amount <= auction.price:
                        raise ValueTooSmallError
                    add_amount = Bid.objects.create(amount=amount, auction_id=auction, user_id=request.user)
                    Listings.objects.filter(id__in=[auction.id]).update(price=amount)
                    return HttpResponseRedirect(reverse('auction', args=[auction.id]))
                except ValueTooSmallError:
                    return render(request, 'auctions/not_found.html', {
                        "title_error":"Bid Error",
                        "message_error":"Your bid has to be bigger than the actual bid."
                    })

    return render(request, 'auctions/auction.html', {
        'auction': auction,
        'in_watch': in_watch,
        'add_bid': add_bid
    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, 'auctions/watchlist.html', {
        'user': user,
        'user_watchlist': watchlist
    })
