
from django.contrib.auth.models import AbstractUser
from django.db import models

# store Log in details and passwords for authentication 
# Also stores the User Information 



class User(AbstractUser):
    pass

class ItemCategory (models.Model):
    ItemCategoryName=models.CharField('Cat Name', max_length=20)
    def __str__(self):
        return f"{self.ItemCategoryName}"

# store auction listings - create listing 
class Listing (models.Model):
    Title=models.CharField(max_length=64)
    Artist=models.CharField(max_length=64)
    Description = models.TextField(blank=True)
    StartBidAmount=models.FloatField()
    Image=models.ImageField(upload_to='listing', blank=True ,null=True) #null back end blank front end
    ItemCategory=models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    ListedOn= models.DateTimeField(auto_now_add=True)
    Status=models.BooleanField(default=True)
    ListedBy= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.Title

    def max_bid(self):
        data = Listing.objects.filter(id=self.id).annotate(max=models.Max('bid__Amount'))
        print(data[0])
        return data[0].max



class Bid(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    BidBy=models.ForeignKey(User, on_delete=models.CASCADE)
    Amount=models.FloatField()
    BidOn= models.DateTimeField(auto_now_add=True)
    BidWon=models.BooleanField(default=False)            #new field to populate yes when this is the last bid


class Comment(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    CommentBy=models.ForeignKey(User, on_delete=models.CASCADE)
    Comment=models.TextField()
    CommentOn= models.DateTimeField(auto_now_add=True)

class WatchList(models.Model):
    listing=models.ForeignKey(Listing,on_delete=models.CASCADE)
    WatchListOf=models.ForeignKey(User, on_delete=models.CASCADE)



   






