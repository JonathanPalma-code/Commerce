from .models import Auction, Bid
from django import forms

from .models import Category, Bid

class AddAuction(forms.Form):
    title = forms.CharField(label='', max_length=64, widget=forms.TextInput(attrs={
        'placeholder': 'Title', 
        'class' : 'add-form__title form-control'
        }))
    description = forms.CharField(label='', max_length=800, widget=forms.Textarea(attrs={
        'placeholder': 'Description',
        'rows' : 10, 
        'class' : 'add-form__description form-control'
        }))
    category = forms.ModelChoiceField(label='', initial=1, queryset=Category.objects.all(), required=True, widget=forms.Select(attrs={
        'class' : 'add-form__category form-control'
    }))
    price = forms.DecimalField(label='', min_value=0, widget=forms.NumberInput(attrs={
        'placeholder': 'Bid', 
        'class' : 'add-form__price form-control'
        }))
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
    category = forms.ModelChoiceField(label='', queryset=Category.objects.all(), required=True, widget=forms.Select(attrs={
        'class' : 'form-control col-2'
    }))
        