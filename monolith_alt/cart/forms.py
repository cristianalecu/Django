from django import forms
from shop.models import Product, UnitMeasure
from dal import autocomplete

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

class CartAddProductForm(forms.Form):
	product_name = forms.ModelChoiceField(queryset=Product.objects.all(), 
		widget=autocomplete.ModelSelect2(url='shop:product-autocomplete', attrs={'class': 'modern-style', 'data-placeholder': 'Search...',},))

	PRODUCT_UM_CHOICES = UnitMeasure.objects.all().values_list('id', 'name')
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, required=False)
	um = forms.TypedChoiceField(choices=PRODUCT_UM_CHOICES, coerce=int, required=False)
	update = forms.BooleanField(required=False,initial=False, widget=forms.HiddenInput)