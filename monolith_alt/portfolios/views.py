from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.forms import modelformset_factory

from .models import Portfolio, PortfolioProduct, CustomerPortfolio
from .forms import ProductForm, PortfolioForm
from users.models import Profile, Customer
from cart.cart import Cart
from shop.models import UnitMeasure, Product, Supplier
from portfolios.models import CustomerPortfolioProduct, CustomerPortfolio
from portfolios.forms import CustomerPortfolioForm

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

def customer_portfolio_list(request):
	if not request.user.is_authenticated:
		return redirect('users:login')
	objs = CustomerPortfolio.objects.filter(user=request.user)
	args = {
		'title': 'Customer Portfolios',
		'link_new': 'portfolios:customer_portfolio_new',
		'link_edit': 'portfolios:customer_portfolio_edit',
		'link_delete': 'portfolios:customer_portfolio_delete',
		'fields': ['name', 'supplier', 'customer'],
		'objs': objs,
		'no_objects_msg': 'You have no Customer Portfolios',
		}
	return render(request, 'shop/sheet.html', args)

def customer_portfolio_new(request):
	if not request.user.is_authenticated:
		return redirect('users:login')
	CustPortfolioProdFormSet = modelformset_factory(
		CustomerPortfolioProduct, 
		fields=('product', 'price', 'quantity', 'um'), 
		can_delete=True,
		extra=1)
	if request.method == "POST":
		form = CustomerPortfolioForm(request.POST)
		formset = CustPortfolioProdFormSet(request.POST, request.FILES)
		if form.is_valid() and formset.is_valid() :
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			instances = formset.save(commit=False)
			for instance in instances:
				instance.user = request.user
				instance.portfolio = obj
				instance.save()
			formset.save(commit=True)
			return redirect('portfolios:customer_portfolio_list')
	else:
		form = CustomerPortfolioForm()
		formset = CustPortfolioProdFormSet(queryset=CustomerPortfolioProduct.objects.none())

	form.fields['supplier'].queryset = Supplier.objects.filter(user=request.user)
	form.fields['customer'].queryset = Customer.objects.filter(user=request.user)
	args = {
		'form_title': 'Customer Portfolio',
		'formset_title': 'Portfolio items',
		'link_new': 'portfolios:customer_portfolio_new',
		'link_edit': 'portfolios:customer_portfolio_edit',
		'link_delete': 'portfolios:customer_portfolio_delete',
		'form': form,
		'formset': formset,
		}
	return render(request, 'shop/form_formset_edit.html', args)

def customer_portfolio_edit(request, pk):
	if not request.user.is_authenticated:
		return redirect('users:login')
	obj = get_object_or_404(CustomerPortfolio, pk=pk)
	CustPortfolioProdFormSet = modelformset_factory(
		CustomerPortfolioProduct, 
		fields=('product', 'price', 'quantity', 'um'), 
		can_delete=True,
		extra=1)
	if request.method == "POST":
		form = CustomerPortfolioForm(request.POST, instance=obj)
		formset = CustPortfolioProdFormSet(request.POST, request.FILES, queryset=CustomerPortfolio.objects.filter(portfolio=obj))
		if form.is_valid() and formset.is_valid() :
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			instances = formset.save(commit=False)
			for instance in instances:
				instance.user = request.user
				instance.author = obj
				instance.save()
				instance.portfolio = obj
				instance.save()
			formset.save(commit=True)
			return redirect('portfolios:customer_portfolio_list')
	else:
		form = CustomerPortfolioForm(instance=obj)
		formset = CustPortfolioProdFormSet(queryset=CustomerPortfolioProduct.objects.filter(portfolio=obj))

	form.fields['supplier'].queryset = Supplier.objects.filter(user=request.user)
	form.fields['customer'].queryset = Customer.objects.filter(user=request.user)
	args = {
		'form_title': 'Customer Portfolio',
		'formset_title': 'Portfolio items',
		'link_new': 'portfolios:customer_portfolio_new',
		'link_edit': 'portfolios:customer_portfolio_edit',
		'link_delete': 'portfolios:customer_portfolio_delete',
		'form': form,
		'formset': formset,
		}
	return render(request, 'shop/form_formset_edit.html', args)

def customer_portfolio_delete(request, pk):
	obj = get_object_or_404(CustomerPortfolio, pk=pk)
	obj.delete()
	return redirect('portfolios:customer_portfolio_list')