from django import forms
from .models import Listing

class listingform(forms.ModelForm):
    class Meta:
        model=Listing
        exclude=('Status','ListedBy','ListedOn')

