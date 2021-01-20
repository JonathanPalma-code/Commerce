from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from django.db.models import Max

from .forms import AddAuction, AddBid, AddComment, CategoryOption
from .models import User, Bid, Auction, Comment, Category, Watchlist, Product
from datetime import datetime

from django.db.models import Exists

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
    auction = Auction.objects.exclude(active=False).all().order_by('-id')
    query_wachlist = None

    if request.user.is_authenticated:
        query_wachlist = Watchlist.objects.filter(user=request.user, auction__in=auction)

    if request.method == "POST":
        form = CategoryOption(request.POST)
        queryset = Product.objects.filter(category = form['category'].value())
        dynamic_search = Auction.objects.exclude(active=False).filter(product__in=queryset).order_by('-id')

        return render(request, "auctions/index.html", {
            'auction_listings': dynamic_search,
            'category_option': form
        })

    return render(request, "auctions/index.html", {
        'auction_listings': auction,
        'category_option': CategoryOption(),
        'in_watchlist': query_wachlist
    })

@login_required
def add(request):
    if request.method == 'POST':
        form = AddAuction(request.POST, request.FILES)
        if form.is_valid():
            date = datetime.now().isoformat(' ', 'seconds')
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            price = form.cleaned_data['price']
            category = form.cleaned_data['category']
            url = form.cleaned_data['url']
            product = Product.objects.create(title=title, description=description, price=price, category=category, url=url, date_posted=date, creator=request.user)
            auction = Auction.objects.create(product=product)
            bid = Bid.objects.create(amount=product.price, auction=auction, user=request.user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/add', {
                'add_auction_form': form
            })
    return render(request, 'auctions/add.html', {
        'add_auction_form': AddAuction()
    })

def auction(request, auction_id):
    auction = Auction.objects.get(pk=auction_id)
    comments = Comment.objects.filter(auction=auction.id)
    in_watch = None
    add_bid = auction.product.price
    bid_username = None
    winner = None
    comment = None
    
    if request.user.is_authenticated:
        in_watch = Watchlist.objects.filter(user=request.user, auction=auction)
        add_bid = AddBid()

        if request.method == 'POST' and 'watchlist_btn' in request.POST:
            if in_watch:
                in_watch.delete()
                return HttpResponseRedirect(reverse('auction', args=[auction_id]))
            else:
                add_wathlist = Watchlist.objects.create(user=request.user, auction=auction)
                return HttpResponseRedirect(reverse('auction', args=[auction_id]))
        
        if request.method == 'POST' and 'bid_btn' in request.POST:
            form = AddBid(request.POST)
            if form.is_valid() and auction.active:
                try: 
                    amount = form.cleaned_data['amount']
                    if amount <= auction.product.price:
                        raise ValueTooSmallError
                    add_amount = Bid.objects.create(user=request.user, auction=auction, amount=amount)
                    Product.objects.filter(id__in=[auction.product.id]).update(price=amount)
                    return HttpResponseRedirect(reverse('auction', args=[auction.id]))
                except ValueTooSmallError:
                    return render(request, 'auctions/not_found.html', {
                        "title_error":"Bid Error",
                        "message_error":"Your bid has to be bigger than the actual bid."
                    })
        
        bid_username = Bid.objects.filter(auction_id=auction.id).first().user
        winner = Bid.objects.filter(auction_id=auction.id).last().user
        if bid_username and request.method == 'POST' and 'close_btn' in request.POST:
            Auction.objects.filter(id__in=[auction.id]).update(winner=str(winner), active=False)
            return HttpResponseRedirect(reverse('auction', args=[auction.id]))

        if request.method == 'POST' and 'comment_btn' in request.POST:
            form = AddComment(request.POST)
            if form.is_valid():
                comment = form.cleaned_data['comment']
                Comment.objects.create(description=comment, auction=auction, user=request.user)
                return HttpResponseRedirect(reverse('auction', args=[auction.id]))

    return render(request, 'auctions/auction.html', {
        'auction': auction,
        'in_watch': in_watch,
        'add_bid': add_bid,
        'bid_user_name': bid_username,
        'winner': winner,
        'add_comment': AddComment(),
        'comments': comments.order_by('-time_sent')

    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    watchlist = Watchlist.objects.filter(user=user)
    return render(request, 'auctions/watchlist.html', {
        'user': user,
        'user_watchlist': watchlist
    })
