from django import forms
from django.forms import widgets

from .models import Bid, Listings, Comment

class NewListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ['Title', 'Description', 'StartPrice', 'Photo', 'Category']
        widgets = {
            'Title': forms.TextInput(attrs={'class': 'form-control'}),
            'Description': widgets.Textarea(attrs={'cols' : 60, 'rows' : 10, 'class' : 'form-control'}),
            'StartPrice': forms.NumberInput(attrs={'class': 'form-control'}),
            'Photo': forms.URLInput(attrs={'class': 'form-control'}),
            'Category': widgets.Select(attrs={'calss': 'form-control'})
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['Comment']
        widgets = {
            'Comment': widgets.Textarea(attrs={'cols' : 60, 'rows' : 10, 'class' : 'form-control'})
        }

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['Amount']
        widgets = {
            'Amount' : forms.NumberInput(attrs={'class': 'form-control'})
        }