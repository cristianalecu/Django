#gui/views.py
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string
from django.core import serializers
from dal import autocomplete
from tablib import Dataset
from slugify import slugify

from cart.forms import CartAddProductForm
from cart.cart import Cart
from orders.forms import OrderCreateForm
from orders.views import get_orders_of_user, chart_ordered_products, get_chart_ordered_amounts
from users.views import get_favorite_products

from .models import Category, Product, Supplier
from .resources import ProductResource
from users.models import Customer
from orders.models import SupplierOrder

def product_list(request, criteria_slug=None):
	category = None
	products = Product.objects.filter(available=True)
	
	if criteria_slug:
		try:
			category = Category.objects.get(slug=criteria_slug)
			products = products.filter(category=category)
			return render(request, 'shop/product/list.html', {'category': category,'products': products})
		except Category.DoesNotExist:
			pass

		try:
			supplier = Supplier.objects.get(slug=criteria_slug)
			products = products.filter(supplier=supplier)
			return render(request, 'shop/product/list.html', {'supplier': supplier, 'products': products})
		except Supplier.DoesNotExist:
			pass
			
	return render(request, 'shop/product/list.html', {'category': category, 'products': products})

def product_detail(request, id, slug):

	product = get_object_or_404(Product, id=id, slug=slug, available=True)
	cart_product_form = CartAddProductForm()

	return render(request, 'shop/product/detail.html', {'product': product,'cart_product_form': cart_product_form})

@login_required()
def dashboard(request):
	orders = get_orders_of_user(request.user)
	# favorites = get_favorite_products(request.user)
	# chart_qty = chart_ordered_products(request.user)
	# chart_amount = get_chart_ordered_amounts(request.user)
	# return render(request, 'shop/dashboard.html', {'orders': orders, 'products':favorites, 'chart_qty':chart_qty, 'chart_amount':chart_amount})
	cart = Cart(request)
	for item in cart:
		print(item)
		item['update_form'] = CartAddProductForm(initial={'product_name': item['product'].id, 'quantity': item['quantity'], 'um': item['um'], 'update': True})

	quick_submit_form = OrderCreateForm()
	
	custID = int(request.session.get("customer_selected", '0'))
	if custID > 0:
		cust = get_object_or_404(Customer, id=custID)
		quick_submit_form.initial['customer'] = custID
		quick_submit_form.initial['first_name'] = cust.first_name
		quick_submit_form.initial['last_name'] = cust.last_name
		quick_submit_form.initial['email'] = cust.email
		quick_submit_form.initial['address'] = cust.address
		quick_submit_form.initial['phone'] = cust.phone
	
	# quick_submit_form.initial['first_name'] = request.user.first_name
	# quick_submit_form.initial['last_name'] = request.user.last_name
	# quick_submit_form.initial['email'] = request.user.email
	# if request.user.profile:
	# 	quick_submit_form.initial['address'] = request.user.profile.address
	# 	quick_submit_form.initial['phone'] = request.user.profile.phone

	return render(request, 'shop/dashboard.html', {'orders': orders, 'search_form': CartAddProductForm, 'cart': cart, 'quick_submit_form':quick_submit_form})#, {'orders': orders, 'products':favorites, 'chart_qty':chart_qty, 'chart_amount':chart_amount})

def get_supplier_products(self, pk):
	products = Product.objects.filter(supplier_id=pk)
	return HttpResponse(serializers.serialize('json',products), content_type="application/json")

def get_products(self, supplier_id):
	products = Product.objects.filter(supplier=supplier_id)
	return HttpResponse(serializers.serialize('json',products), content_type="application/json")


def product_import(request):
	context = {}
	if request.method == 'POST':
		product_resource = ProductResource()
		dataset = Dataset()
		new_products_file = request.FILES['products_file']
		string_file = new_products_file.read().decode()
		page_result={}
		items = []
		try:
			imported_data = dataset.load(string_file, format='csv')
			# result = product_resource.import_data(dataset, dry_run=True)  # Test the data import
			# if not result.has_errors():
			page_result['message']="Success! The following items were imported:"
			for row in dataset.dict:
				product = Product()
				product.category = Category.objects.get(id=row['category'])
				product.supplier = Supplier.objects.get(id=row['supplier'])
				product.name = row['name']
				product.slug = slugify(row['name'])
				product.description = row['description']
				product.price = row['price']
				product.stock = row['stock']
				
				product.save()
				items.append(product)
		except Exception:
			page_result['error']="Error while importing items!"

			# product_resource.import_data(dataset, dry_run=False)  # Actually import now
		# else:
		# 	page_result['message']="Error while importing items"

		if items: page_result['items'] = items
		context['result'] = page_result
	return render(request, 'shop/product/import.html', context)




class ProductAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Product.objects.none()

		qs = Product.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs


class SupplierAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Supplier.objects.none()

		qs = Supplier.objects.all()

		if self.q:
			qs = qs.filter(name__istartswith=self.q)

		return qs
	
def mySupplierOrders(request):
	objs = SupplierOrder.objects.filter(user=request.user)
	return render(request, 'shop/sheet.html', {'objs': objs})

