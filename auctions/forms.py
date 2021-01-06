from .models import Auction, Bid
from django import forms

from .models import Category, Bid

class AddAuction(forms.Form):
    title = forms.CharField(label='', max_length=64, widget=forms.TextInput(attrs={
        'placeholder': 'Title', 
        'class' : 'form-control col-md-8 col-lg-8'
        }))
    description = forms.CharField(label='', max_length=800, widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'rows' : 10, 
        'class' : 'form-control col-md-8 col-lg-8'
        }))
    price = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Bid', 
        'class' : 'form-control col-md-4 col-lg-4'
        }))
    category = forms.ModelChoiceField(widget=forms.Select, initial=1, queryset=Category.objects.all(), required=True)
    url = forms.ImageField(label='', required=False)

class AddBid(forms.Form):
    amount = forms.IntegerField(label='', widget=forms.NumberInput(attrs={
        'placeholder': 'Bid', 
        'class' : 'form-control'
        }))

class AddComment(forms.Form):
    comment = forms.CharField(label='Comment', max_length=500, widget=forms.Textarea(attrs={ 
        'rows' : 4, 
        'class' : 'form-control'
        }))

class CategoryOption(forms.Form):
    category = forms.ModelChoiceField(label='', widget=forms.Select, queryset=Category.objects.all(), required=True)
        