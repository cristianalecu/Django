from django import forms

from .models import Order
from users.models import Customer
from orders.models import SupplierOrder

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
		
class SupplierOrderForm(forms.ModelForm):
	class Meta:
		model = SupplierOrder
		fields = ['supplier', 'customer', 'first_name', 'last_name', 'email', 'address', 'phone', 'notes']
		labels = {
            'supplier': 'Supplier',
            'customer': 'Customer',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'address': 'Address',
            'phone': 'Phone',
            'notes': 'Notes',
        }
		help_texts = {
            'supplier': 'Supplier for all the items in this order',
            'customer': 'Customer to receive the order',
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'address': 'Address',
            'phone': 'Phone',
            'notes': 'Notes about delivering and contact receiving',
        }
