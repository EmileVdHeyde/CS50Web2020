from django import forms
from .models import Listing, Comment , Bid
from django.core.exceptions import ValidationError 

class listingform(forms.ModelForm):
    class Meta:
        model=Listing
        exclude=('Status','ListedBy','ListedOn')

class commentsform(forms.ModelForm):
    class Meta:
        model=Comment
        exclude=('CommentOn','CommentBy','listing')
        
class bidform(forms.ModelForm):
    class Meta:
        model=Bid
        exclude=('BidOn','BidBy','listing','BidWon')
    def __init__(self, *args, **kwargs):
        self.listing = kwargs.pop('listing', None)
        super(bidform, self).__init__(*args, **kwargs)

    def clean(self):
        amount=self.cleaned_data.get('Amount')
        if amount < self.listing.max_bid() or amount < self.listing.StartBidAmount:
            raise ValidationError("Bid value is too small") 
        return self.cleaned_data



    


