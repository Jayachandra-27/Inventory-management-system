from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import InventoryItem,Category


class RegistrationForm(UserCreationForm):
    class Meta:
        model=User
        fields=['username','email','password1','password2']

class InventoryItemForm(forms.ModelForm):
    # category = forms.ModelChoiceField(queryset=Category.objects.all(), initial=0)
    class Meta:
        model=InventoryItem
        fields=['name','quantity','category']