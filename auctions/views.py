import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listings
from .forms import NewListingForm


def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listings.objects.all()
    })
    # return render(request, "auctions/index.html")


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

@login_required
def newListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            form.instance.Author = request.user
            form.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/newListing.html", {
                "form" : form
            })
    form = NewListingForm()
    return render(request, "auctions/newListing.html", {
            "form" : form
        })

def listing(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    user = request.user
    inList = listing.inList(user)
    sth = user == Listings.Author
    return render(request, "auctions/listing.html", {
            "listing" : listing,
            "inList" : inList,
            "sth" : sth
        })
    

def watchlist(request):
    listings = request.user.Watchlist.all()
    return render(request, "auctions/watchlist.html", {
        'listings' : listings
    })

def listingChange(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    inList = listing.inList(request.user)
    if inList:
        request.user.Watchlist.remove(listing)
    else:
        request.user.Watchlist.add(listing)


    
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

def removeWatchlist(request, listing_id):
    user = request.user
    listing = Listings.objects.get(pk=listing_id)
    user.Watchlist.remove(listing)

    return HttpResponseRedirect(reverse("watchlist"))
