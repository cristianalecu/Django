from django import forms
from shop.models import Product, Supplier, UnitMeasure
from .models import PortfolioProduct, Portfolio
from dal import autocomplete


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]


class PortfolioForm(forms.ModelForm):
	name = forms.CharField(label='portfolio_name', widget=forms.TextInput(attrs={'placeholder': 'Portfolio name'}))
	supplier = forms.ModelChoiceField(queryset=Supplier.objects.all(), empty_label="Select a supplier")
		# widget=autocomplete.ModelSelect2(url='shop:supplier-autocomplete', 
		# attrs={'data-placeholder': 'Search...','data-minimum-input-length': 1,},))
	class Meta:
		model = Portfolio
		fields = ['name', 'supplier',]

class ProductForm(forms.Form):
	product = forms.ModelChoiceField(queryset=Product.objects.all(), )
		# widget=autocomplete.ModelSelect2(url='shop:product-autocomplete', 
		# attrs={'data-placeholder': 'Search...','data-minimum-input-length': 1,},))

	def __init__(self, *args, **kwargs):
		super(ProductForm, self).__init__(*args, **kwargs)
		self.fields['product'].choices = list(Product.objects.values_list('id', 'name'))

	PRODUCT_UM_CHOICES = UnitMeasure.objects.all().values_list('id', 'name')
	quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int, required=True)
	um = forms.TypedChoiceField(choices=PRODUCT_UM_CHOICES, coerce=int, required=True)

	class Meta:
		model = PortfolioProduct
		fields = ['product', 'quantity', 'um',]