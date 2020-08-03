

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest , Http404 
from django.shortcuts import render , redirect
from django.urls import reverse

from .models import User, Listing , Bid, Comment , WatchList, ItemCategory

 
from .forms import listingform, commentsform

#Index Page all listings, should be tweeked to only show ACTIVE , STATUS conditional 
def index(request):
    #if Listing.Status=True 
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(Status=True)   #Listing.objects.exclude(Listing.Status=False).all()
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


# This is the main view for the listing details , we also want to pull in bid and comment info on the listing page
def listing(request,listing_id):
    try:
         listing =  Listing.objects.get(id=listing_id)       #one listing 
         if WatchList.objects.filter(listing=listing, WatchListOf=request.user).exists():
             added=True
         else:
             added=False
         cform=commentsform()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {'listing':listing , 'cform':cform ,'added':added })

def postcomment(request,pk):
    listing=Listing.objects.get(id=pk)
    cform=commentsform(request.POST)
    if cform.is_valid():
        comment=cform.save(commit=False)
        comment.CommentBy=request.user
        comment.listing=listing
        comment.save()
        return redirect('listing',listing_id=pk)

def addwatchlist (request,pk):
    listing=Listing.objects.get(id=pk)
    if WatchList.objects.filter(listing=listing, WatchListOf=request.user).exists():
       WatchList.objects.filter(listing=listing, WatchListOf=request.user).delete()
    else:
        watchlist=WatchList(listing=listing, WatchListOf=request.user)
        watchlist.save()
    return redirect('listing',listing_id=pk)



#temp=Listing
#print(temp.max_bid(2))
#print(Comment.objects.filter(id=2).values()) 

#view for listing categories , should redirect to the active listings 
def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": ItemCategory.objects.all()
    })

# View to sow the relationship between user and item and show watch list selected 
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "listings": Listing.objects.all()
    })

#View to show FORM to take in the information to populate a new listing
def addlisting(request):
    if request.method=='GET':
        lform=listingform()
        return render (request,'auctions/addlisting.html',{'lform':lform})
    else:
        lform=listingform(request.POST , request.FILES)
        if lform.is_valid():
            listing=lform.save(commit=False)
            listing.ListedBy=request.user
            listing.save()
            return redirect('index')
        return render (request,'auctions/addlisting.html',{'lform':lform})

# Categories Index Page all listings active and in the chosen category in the view category
def categoriesindex(request,id):
    ItemCategoryvar= ItemCategory.objects.filter(id=id).last()
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(Status=True , ItemCategory=ItemCategoryvar)   
    })









# This should take a bid value added on listing page and asses if it is larger than current max bid for item
# If not , do not save, and tell user it value to small
# If larger , save value, save username, save item name into BID model
# automatically this should update the max value of the item. 

#function to show all transactions on all bids in a table for reference , admin user only 
def bidtransaction(request):
    bid=Bid.objects.all()
    return render(request, "auctions/bidhistory.html", {'bid':bid }) 

