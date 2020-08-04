

from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect,HttpResponseBadRequest , Http404 
from django.shortcuts import render , redirect
from django.urls import reverse
from django.core.exceptions import ValidationError 

from .models import User, Listing , Bid, Comment , WatchList, ItemCategory
from .forms import listingform, commentsform, bidform

##################1. ACCESS PAGES - LOG IN , LOG OUT , REGISTER  ###################################################

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



###################2. THE LISTING PAGE ###########################################################

# This is the main view for the listing details, One page per item is generated, using the id of the item. 
# ERROR Control done if the number of listing is not valid.
# Using the relationship between Listing and comments , we call the comments in HTML 
# On this view a comments EMPTY form is also displayed.
# A check for Watch list item added or not is done by the varible ADDED to display different text in HTML <ON/OFF>

def listing(request,listing_id):
    try:
         listing =  Listing.objects.get(id=listing_id)       
         if WatchList.objects.filter(listing=listing, WatchListOf=request.user).exists():
             added=True
         else:
             added=False
         if Listing.objects.filter(Title=listing, ListedBy=request.user, Status=True).exists():
             close=True
         else:
             close=False
         if Listing.objects.filter(Title=listing, ListedBy=request.user).exists():
             myitem=True
         else :
             myitem=False   
         cform=commentsform()
         bform=bidform()
    except Listing.DoesNotExist:
        raise Http404("Listing not found.")
    return render(request, "auctions/listing.html", {'listing':listing , 'cform':cform ,'added':added , 'bform':bform,'close':close,'myitem':myitem })


# While the above view showed the blank template , the below view saves the input into the comments table
# the form only takes comments and automatically we parse the user and listing name to the  comments table 
def postcomment(request,pk):
    listing=Listing.objects.get(id=pk)
    cform=commentsform(request.POST)
    if cform.is_valid():
        comment=cform.save(commit=False)
        comment.CommentBy=request.user
        comment.listing=listing
        comment.save()
        return redirect('listing',listing_id=pk)

# While the view listing showed the blank form to input text, the below view saves the input value to the bid table
# The form will take the user listing name automatrically into comments table
# There needs to be a check to accept the bid , it must be more that the current bid. 
# display a success or not enough message and allow user to add another value in redrect<still need to do

def postbid(request,pk):
    listing=Listing.objects.get(id=pk)
    bform=bidform(request.POST)
    maxbid=listing.max_bid()    #apply this function created in models. apply it to the data object 
    if maxbid is None:
        maxbid=listing.StartBidAmount    # when no bid is placed yet , it myst take the start bid amount 
    if bform.is_valid():
        bid=bform.save(commit=False)
        if bid.Amount>maxbid:
            bid.BidBy=request.user
            bid.listing=listing
            bid.save()
            taken=True
            return redirect('listing',listing_id=pk)
        else:
            taken=False
            raise ValidationError("Bid value is too small") 
    else: 
      taken=False
      return redirect('listing',listing_id=pk)


# remove item from Watchlist  if it exists 
# Add item to watch list , and pass on the listing and user id to the Watchlist table.
def addwatchlist (request,pk):
    listing=Listing.objects.get(id=pk)
    if WatchList.objects.filter(listing=listing, WatchListOf=request.user).exists():
       WatchList.objects.filter(listing=listing, WatchListOf=request.user).delete()
    else:
        watchlist=WatchList(listing=listing, WatchListOf=request.user)
        watchlist.save()
    return redirect('listing',listing_id=pk)


#close bid , only if the you are the lister should this be displayed <ListedBy>
# alow to post the status in listing to Status=0 
#This only updates one record in a table , not as previous adding a row. 
def closeBid(request, pk):
    listing=Listing.objects.get(id=pk)
    bidwon=Bid.objects.filter(id=pk).last()
    if  Listing.objects.filter(Title=listing, ListedBy=request.user, Status=True).exists():
        Listing.objects.filter(Title=listing, ListedBy=request.user, Status=True).update(Status=False)
        bidwon.BidWon = True
        bidwon.save(update_fields=["BidWon"]) #not working properly 
    return redirect('listing',listing_id=pk)    


        

   

############### 3 . ADDING A LISTING ######################################################################

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


###########  4. INDEX PAGE  ###################################################


#Index Page all listings. Filter applied to Listing Model to only show Active Listings
def index(request):
    #if Listing.Status=True 
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(Status=True)   #Listing.objects.exclude(Listing.Status=False).all()
    })


###########  5. CATEGORY  AND CATEGORY INDEX PAGES  ###################################################

#view for listing categories , should redirect to the active listings 
def categories(request):
    return render(request, "auctions/categories.html",{
        "categories": ItemCategory.objects.all()
    })

# Categories Index Page all listings active and in the chosen category in the view category
def categoriesindex(request,id):
    ItemCategoryvar= ItemCategory.objects.filter(id=id).last()
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.filter(Status=True , ItemCategory=ItemCategoryvar)   
    })

###########  5. WATCHLIST PAGE   ###################################################

# View to show the relationship between user and item and show watch list selected 
def watchlist(request):
    return render(request, "auctions/watchlist.html",{
        "watchlistings": WatchList.objects.filter(WatchListOf=request.user)
    })


###################### Bonus 6. BIDDING TRANSACTION PAGE###################################################3

# This should take a bid value added on listing page and asses if it is larger than current max bid for item
# If not , do not save, and tell user it value to small
# If larger , save value, save username, save item name into BID model
# automatically this should update the max value of the item. 


#function to show all transactions on all bids in a table for reference , admin user only
# Add a date filter and an item filter , order by date.  sold filter 
#export to pdf or excel ?? 
def bidtransaction(request):
    bid=Bid.objects.all()
    return render(request, "auctions/bidhistory.html", {'bid':bid }) 

