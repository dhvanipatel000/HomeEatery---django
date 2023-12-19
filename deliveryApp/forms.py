from django import forms
from deliveryApp.models import *

class Food_items_form(forms.ModelForm):

    class Meta:
        model = food_items
        fields = '__all__'
        widgets = {
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'category':forms.Select(attrs={'class':'form-control'}),
            'desc':forms.Textarea(attrs={'class':'form-control'}),
            'price':forms.NumberInput(attrs={'class':'form-control'}),
            'img':forms.FileInput(attrs={'class':'form-control'}),
        }

class CheckoutForm(forms.Form):
    addressline1 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
    }))
    addressline2 = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
    }))
    state = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
    }))

