from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Bid, Listings, Comments, Category, Watchlist

class AddAuction(forms.Form):
    title = forms.CharField(label='', max_length=64, widget=forms.TextInput(attrs={
        'placeholder': 'Title', 
        'class' : 'form-control col-md-8 col-lg-8'
        }))
    description = forms.CharField(label='', max_length=300, widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'rows' : 10, 
        'class' : 'form-control col-md-8 col-lg-8'
        }))
    bid = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Bid', 
        'class' : 'form-control col-md-4 col-lg-4'
        }))
    category = forms.ModelChoiceField(widget=forms.Select, initial=1, queryset=Category.objects.all(), required=True)
    url = forms.ImageField(label='', required=False)


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
        'listings': Listings.objects.all()
    })

@login_required
def add(request):
    if request.method == 'POST':
        form = AddAuction(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            bid = form.cleaned_data['bid']
            category = form.cleaned_data['category']
            url = form.cleaned_data['url']
            bid_bd = Bid.objects.create(amount=bid)
            bid_id = Bid.objects.get(pk=bid_bd.id)
            listing = Listings.objects.create(title=title, description=description, bid=bid_id, category=category, url=url)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'auctions/add', {
                'add_auction_form': form
            })
    return render(request, 'auctions/add.html', {
        'add_auction_form': AddAuction()
    })

@login_required
def auction(request, auction_id):
    auction = Listings.objects.get(pk=auction_id)
    in_watch = Watchlist.objects.filter(user=request.user, product=auction)

    if request.method == 'POST':
        if Watchlist.objects.filter(user=request.user, product=auction):
            Watchlist.objects.filter(user=request.user.id, product=auction.id).delete()
            return HttpResponseRedirect(reverse('index'))
        else:
            add_wathlist = Watchlist.objects.create(user=request.user, product=auction)
            return HttpResponseRedirect(reverse('watchlist', args=[request.user.id]))
        
    return render(request, 'auctions/auction.html', {
        'auction': auction,
        'in_watch': in_watch
    })

@login_required
def watchlist(request, user_id):
    user = User.objects.get(pk=user_id)
    watchlist = Watchlist.objects.all()
    return render(request, 'auctions/watchlist.html', {
        'user': user,
        'user_watchlist': watchlist
    })
