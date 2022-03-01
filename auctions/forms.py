from django import forms
from django.forms import widgets

from .models import Category, Bids, Comment, Listings

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['Title', 'Description', 'StartPrice', 'Photo', 'Category']
        widgets = {
            'Description':widgets.Textarea(attrs={'cols' : 80, 'rows' : 20, 'class' : 'form-control'}),
        }