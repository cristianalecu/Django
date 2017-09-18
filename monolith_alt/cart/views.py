from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from django.contrib import messages
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from django.template.context_processors import request

@require_POST
def cart_add(request, product_id=None):
	cart = Cart(request)
	form = CartAddProductForm(request.POST)
	custID = request.POST["add_customer_selected"]
	if custID:
		if int(custID) > 0 :
			request.session["customer_selected"] = custID;
			request.session.modified = True	
	if product_id:
		product = get_object_or_404(Product, id=product_id)
	else:
		product = get_object_or_404(Product, id=request.POST['product_name'])
	msg = ""
	if form.is_valid():
		cd = form.cleaned_data
		if not isinstance(cd['quantity'], int):
			cd['quantity'] = 1

		p_id = str(product.id)
		if p_id not in cart.cart.keys():
			msg = "Product successfully added!"
		else:
			msg = "Product successfully updated!"

		cart.add(product=product, quantity=cd['quantity'], um=cd['um'], update=cd['update'])
		return redirect(request.META.get('HTTP_REFERER'), messages.success(request, msg, 'alert-success'))
	else :
		print(form.errors)
		return redirect(request.META.get('HTTP_REFERER'), messages.error(request, form.errors, 'alert-success'))

def cart_remove(request, product_id):
	cart = Cart(request)
	product = get_object_or_404(Product, id=product_id)
	custID = request.POST["del_customer_selected"]
	if custID:
		if int(custID) > 0 :
			request.session["customer_selected"] = custID;
			request.session.modified = True	
	cart.remove(product)
	msg = "Product removed!"
	return redirect(request.META.get('HTTP_REFERER'), messages.success(request, msg, 'alert-success'))

def cart_detail(request):
	cart = Cart(request)
	for item in cart:
		item['update_form'] = CartAddProductForm(initial={'quantity': item['quantity'],'update': True})

	return render(request, 'cart/detail.html', {'cart': cart})