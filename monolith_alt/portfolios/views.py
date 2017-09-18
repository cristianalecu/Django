from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.db import IntegrityError

from .models import Portfolio, PortfolioProduct
from .forms import ProductForm, PortfolioForm
from users.models import Profile
from cart.cart import Cart
from shop.models import UnitMeasure, Product

def portfolio_list(request):
	if request.user.is_authenticated:
		ProductFormSet = formset_factory(ProductForm)
		portfolios = Portfolio.objects.filter(user=request.user.profile)
	
		portfolio_form = PortfolioForm()
		product_formset = ProductFormSet()

	context = {
		'portfolios': portfolios,
		'portfolio_form': portfolio_form,
		# 'product_formset': product_formset,
	}
	return render(request, 'portfolios/product/list.html', context)

def portfolio_detail(request, id):
	portfolio = get_object_or_404(Portfolio, id=id)

	return render(request, 'portfolios/product/detail.html', {'portfolio': portfolio,})


def portfolio_add(request):
	if request.user.is_authenticated:
		# ProductFormSet = formset_factory(ProductForm)
		portfolios = Portfolio.objects.filter(user=request.user.profile)
		if request.method == 'POST':
			portfolio_form = PortfolioForm(request.POST)
			# product_formset = ProductFormSet(request.POST)

			if portfolio_form.is_valid(): #and product_formset.is_valid():
				portfolio = portfolio_form.save(commit=False)
				portfolio.user = Profile.objects.get(user=request.user)
				portfolio_form.save()

				# print(request.POST['selected_products'])
				values = map(int, request.POST['selected_products'].split(','))
				products = []
				for product in values:
					# product = product_form.cleaned_data.get('product')
					# quantity = product_form.cleaned_data.get('quantity')
					# um = product_form.cleaned_data.get('um')
					if product:
						products.append(PortfolioProduct(portfolio=portfolio, product=Product.objects.get(id=product), quantity=1, um=UnitMeasure.objects.get(id=1)))

				try:
					PortfolioProduct.objects.bulk_create(products)

					# And notify our users that it worked
					messages.success(request, 'Portfolio added succesfully!', 'alert-success')

				except Exception as e: #If the transaction failed
					print(e)
					messages.error(request, 'Error saving portfolio!', 'alert-danger')
			else:
				messages.error(request, 'Error saving portfolio!', 'alert-danger')

	return redirect('portfolios:portfolio_list')


def portfolio_delete(request, portfolio_id):
	portfolio = Portfolio.objects.get(id=portfolio_id, user=request.user.profile)
	portfolio.delete()
	return redirect(request.META.get('HTTP_REFERER'), messages.success(request, "Portfolio was successfully deleted!", 'alert-success'))

def portfolio_order(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			portfolio = get_object_or_404(Portfolio, id=request.POST['portfolio_id'])
			cart = Cart(request)
			cart.clear()
			for product in portfolio.products.all():
				prod = product.product
				cart.add(prod, um=product.um.id, quantity=product.quantity)
	return redirect('dashboard')
