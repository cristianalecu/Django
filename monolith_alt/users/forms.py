from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Customer

class SignUpForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Required. Input a valid email address.')
	first_name = forms.CharField(max_length=30)
	last_name = forms.CharField(max_length=30)
	address = forms.CharField(max_length=250)
	postal_code = forms.CharField(max_length=20, required=False, help_text='Optional.')
	city = forms.CharField(max_length=100)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'address', 'postal_code', 'city', 'password1', 'password2', )


class CustomerForm(forms.ModelForm):
	first_name = forms.CharField(max_length=40, label='first_name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
	last_name = forms.CharField(max_length=40, label='last_name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
	address = forms.CharField(max_length=250, label='address', widget=forms.TextInput(attrs={'placeholder': 'Address'}))
	city = forms.CharField(max_length=20, label='city', widget=forms.TextInput(attrs={'placeholder': 'City'}))
	phone = forms.CharField(max_length=20, label='phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
	email = forms.EmailField(max_length=40, help_text='Required. Input a valid email address.', label='email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))

	class Meta:
		model = Customer
		fields = ('first_name', 'last_name', 'address', 'city', 'phone', 'email', )