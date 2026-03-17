from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Listing

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'display_name')

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'category', 'price', 'pickup_location', 'description']