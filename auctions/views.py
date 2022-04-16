import re
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Listings, Comment, Category, Bid
from .forms import NewListingForm, CommentForm, BidForm


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

@login_required(login_url='login')
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
    if request.method == "POST":
        commentform = CommentForm(request.POST)
        if commentform.is_valid():
            commentform.instance.Listing = listing
            commentform.instance.User = request.user
            commentform.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

    
    commentform = CommentForm()
    bidForm = BidForm()
    comments = Comment.objects.filter(Listing = listing)
    user = request.user
    if user.is_authenticated:
        inList = listing.inList(user)
    else:
        inList = False
    sth = user == Listings.Author
    return render(request, "auctions/listing.html", {
            "listing" : listing,
            "inList" : inList,
            "sth" : sth, 
            "comments" : comments,
            "commentform" : commentform,
            "bidForm" : bidForm
        })
    
@login_required(login_url='login')
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

def category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {"categories" : categories})

def binder(request, category):
    
    category = Category.objects.get(name=category)

    listings = Listings.objects.filter(Category=category)
    return render(request, "auctions/index.html",{
        "listings" : listings
    })

@login_required(login_url='login')
def AddBid(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    if request.method == "POST":
        bidForm = BidForm(request.POST)
        if bidForm.is_valid():
            bidForm.instance.Listing = listing
            bidForm.instance.User = request.user
            if bidForm.instance.Amount > listing.currentPrice():
                bidForm.save()
                messages.success(request, 'Bid added')
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                messages.error(request, 'place a bid higher than the current one')

                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))

@login_required(login_url='login')
def CloseBid(request, listing_id):
    listing = Listings.objects.get(pk=listing_id)
    listing.Active = False
    listing.save()
    messages.success(request, 'Bid closed')
    return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
    



    
   

   
    
        

