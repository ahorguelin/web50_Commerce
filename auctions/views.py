from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Listing, Category, Bid, Comment
from .forms import newListing, newBid, newComment


def index(request):
    #context with all created and active listing
    listing = Listing.objects.filter(active=True)
    listing_bid = []
    for entry in listing:
        if entry.listing_bids.exists():
            listing_bid.append({"listing": entry.title, "amount": entry.listing_bids.latest('bid_date').amount})
        else:
            listing_bid.append({"listing": entry.title, "amount": "No bids yet!"})

    return render(request, "auctions/index.html", {
        "listing": listing,
        "listing_bid": listing_bid
        })

@login_required(login_url='/login')
def create_listing(request):
    #display page with form if users has a get request
    if request.method != "POST":
        return render(request, "auctions/new.html", {
        "newListing": newListing
        })
    

    else:
        form = newListing(request.POST)
        if form.is_valid():
            #get the category and user from the form
            user = User.objects.get(username = request.user.username)

            #check whether category have been added
            if form.cleaned_data["category"]:
                category_id = form.cleaned_data["category"]
                category = Category.objects.get(id = int(category_id[0]))
            else:
                category = None

            #create the record with the remaining information
            listing = Listing(
                owner = user,
                title = form.cleaned_data["title"],
                description = form.cleaned_data["description"],
                category = category,
                starting_bid = form.cleaned_data["starting_bid"],
                img = form.cleaned_data["image"],
                active = True)
            
            #add the record to the db and redirect the user
            listing.save()
            return HttpResponseRedirect(reverse("index"))

        return HttpResponseRedirect(reverse("new"))
    

def view_listing(request, listing_name):
    #get the listing and the bids if any exist
    listing = Listing.objects.get(title = listing_name)
    if listing.listing_bids.exists():
        listing_bid = listing.listing_bids.latest('bid_date').amount
    else:
        listing_bid = None
    
    #get the comment if they exist
    if listing.listing_comments.exists():
        comments = listing.listing_comments.all().order_by('-date')
    else:
        comments = None
    
    #verify whether the current user has the item in their watchlist 
    watcher = listing.user_watchlist.filter(username = request.user.username).exists()
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "listing_bid": listing_bid,
        "listing_comment": comments, 
        "watcher": watcher,
        "bid_form": newBid,
        "comment_form": newComment
    })


@login_required(login_url='/login')
def toggle_watchlist(request, listing_name):
    #get the listing and the user 
    listing = Listing.objects.get(title = listing_name)
    user = User.objects.get(username = request.user.username)

    #check if the user has the item in watchlist
    watcher = listing.user_watchlist.filter(username = request.user.username).exists()

    if watcher:
        #remove the listing item from the watchlist
        user.watchlist.remove(listing)
    else:
        #add the listing item to the user's watchlist
        user.watchlist.add(listing)
    
    #redirect the user to the listing page
    return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))


@login_required(login_url='/login')
def bid(request, listing_name):
    #get the user & the listing
    listing = Listing.objects.get(title = listing_name)
    user = User.objects.get(username = request.user.username)
    if listing.listing_bids.exists():
        latest_bid = listing.listing_bids.latest('bid_date').amount
    else:
        latest_bid = 0

    #get info from forms if the user does a post request
    if request.method == "POST":
        #check for data validity
        form = newBid(request.POST)
        if form.is_valid():
            user_bid = form.cleaned_data["amount"]
            #check if the bid from POST is greater than starting bid or the latest bid
            if (user_bid < listing.starting_bid) or (user_bid < latest_bid):
                #redirect user if their bid is invalid
                #method for error messages found in Django documentation: https://docs.djangoproject.com/en/4.1/ref/contrib/messages/
                messages.add_message(request, messages.INFO, 'Your bid should be higher than the highest bid on the listing.')
                return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))
                                
            bid = Bid(
                owner = user,
                amount = user_bid,
                listing = listing)
            bid.save()
            return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))
        
        else:
            #redirect user if their input is invalid
            messages.add_message(request, messages.INFO, 'You must enter a monetary value to bid on an item.')
            return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))

    #redirect user to listing they were watching
    return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))


@login_required(login_url='/login')
def close_listing(request, listing_name):
    #get the listing and deactivate it
    listing = Listing.objects.get(title = listing_name)
    listing.active = False
    
    #check if the auction had bids
    if listing.listing_bids.exists():
        latest_bidder = listing.listing_bids.latest('bid_date').owner
        listing.winner = latest_bidder

    #save the listing
    listing.save()

    #redirect user to the listing page
    return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))


@login_required(login_url='/login')
def comment_listing(request, listing_name):
    if request.method == "POST":
    #check for data validity
        form = newComment(request.POST)
        if form.is_valid():
            #get data and create the record
            user_comment = form.cleaned_data["comment"]
            comment = Comment(
                owner = User.objects.get(username = request.user.username),
                text = user_comment,
                listing = Listing.objects.get(title = listing_name))
            comment.save()
    
    #redirect the user toward the listing they visited
    return HttpResponseRedirect(reverse("view_listing", kwargs={'listing_name': listing_name}))


@login_required(login_url='/login')
def view_watchlist(request, username):
    #get the user and their watchlist
    user = User.objects.get(username = request.user.username)
    user_watchlist = user.watchlist.all()
    return render(request, 'auctions/watchlist.html', {
    "user_watchlist": user_watchlist
    })


def browse_categories(request):
    categories = Category.objects.all()
    return render(request, 'auctions/categories.html', {
        'categories': categories
    })

def category_listings(request, category_name):
    category_id = Category.objects.get(name = category_name)
    active_listings = Listing.objects.filter(category = category_id, active = True)
    return render(request, 'auctions/category_listings.html', {
        'active_listings': active_listings,
        'category': category_name
    })

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
