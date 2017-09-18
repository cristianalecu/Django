from django import forms

from .models import Order
from users.models import Customer

class OrderCreateForm(forms.ModelForm):
	customer = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label="Select a customer")
	first_name = forms.CharField(label='first_name', widget=forms.TextInput(attrs={'placeholder': 'First name'}))
	last_name = forms.CharField(label='last_name', widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
	email = forms.EmailField(label='email', widget=forms.TextInput(attrs={'placeholder': 'Email'}))
	address = forms.CharField(label='address', widget=forms.TextInput(attrs={'placeholder': 'Address'}))
	phone = forms.CharField(label='phone', widget=forms.TextInput(attrs={'placeholder': 'Phone'}))
	class Meta:
		model = Order
		fields = ['customer', 'first_name', 'last_name', 'email', 'address', 'phone']