from django import forms
from .models import Buyer


class BuyerForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Buyer
        fields = ['username', 'email', 'password', 'full_name', 'address', 'phone']
