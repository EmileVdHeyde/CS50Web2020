from django import forms
from .models import Listing, Comment , Bid

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

    


