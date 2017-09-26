from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Sum, Count, F # does stuff with database field manipulation
from django.http import HttpResponse

from shop.models import UnitMeasure, Supplier, Product
from cart.cart import Cart
from users.models import Customer
from orders.models import SupplierOrder, SupplierOrderItem
from orders.forms import SupplierOrderForm

from .models import Order, OrderItem
from .forms import OrderCreateForm
from .resources import OrderResource, OrderItemResource
from .tasks import create_order
from .pika import create_order2

from django.forms.formsets import formset_factory
from django.forms import modelformset_factory

def order_create(request):
	if not request.user.is_authenticated:
		return redirect('users:login')

	cart = Cart(request)
	if request.method == 'POST':
		form = OrderCreateForm(request.POST)
		if len(cart) == 0:
			return redirect(request.META.get('HTTP_REFERER'), messages.error(request, "Order cannot be empty!", 'alert-warning'))
		if form.is_valid():
			order = form.save(commit=False)
			order.user = request.user
			order.customer = form.cleaned_data['customer']
			order.save()

			#celery
			# create_order.delay(order)

			#pika
			create_order2(Order.objects.get(id=order.id))

		for item in cart:
			unit = UnitMeasure.objects.get(id=item['um'])
			OrderItem.objects.create(order=order, product=item['product'], price=item['price'],	quantity=item['quantity'], um=unit)
			# fav, created = FavoriteProduct.objects.get_or_create(user=request.user.profile, product=item['product'], defaults={'quantity': item['quantity'], 'times_bought':1},)
			# if not created:
			# 	fav.quantity = F('quantity') + item['quantity']
			# 	fav.times_bought = F('times_bought') + 1
			# 	fav.save()

		
		# clear the cart
		cart.clear()
		return redirect(request.META.get('HTTP_REFERER'), messages.success(request, "Order {} added successfully!".format(order.id), 'alert-success'))
		# return render(request, 'orders/created.html', {'order': order}) 
	else:
		form = OrderCreateForm()
		# form.initial['first_name'] = request.user.first_name
		# form.initial['last_name'] = request.user.last_name
		# form.initial['email'] = request.user.email
		# if request.user.profile:
		# 	form.initial['address'] = request.user.profile.address
			
		# 	form.initial['phone'] = request.user.profile.phone

	return render(request,'orders/create.html',{'cart': cart, 'form': form})

def get_orders_of_user(user, customer=None):
	if not user.is_anonymous:
		if customer:
			orders = Order.objects.filter(user=user, customer=customer)
		else:
			orders = Order.objects.filter(user=user)
	else:
		orders = None

	return orders

def order_list(request):
	orders = get_orders_of_user(request.user)
	return render(request, 'orders/list.html', {'orders': orders})

def order_detail(request, order_id):
	order = get_object_or_404(Order, id=order_id, user=request.user)
	products = OrderItem.objects.filter(order=order)
	return render(request, 'orders/detail.html', {'order': order, 'products': products})

# def order_edit(request, order_id):
# 	order = Order.objects.get(id=order_id, user=request.user)
# 	if request.POST:
# 		form = OrderForm(request.POST, instance=order)
# 		if form.is_valid():
# 			if form.save():
# 				return redirect('/', messages.success(request, 'Order was successfully updated.', 'alert-success'))
# 			else:
# 				return redirect('/', messages.error(request, 'Data is not saved', 'alert-danger'))
# 		else:
# 			return redirect('/', messages.error(request, 'Form is not valid', 'alert-danger'))
# 	else:
# 		form = OrderForm(instance=order)
# 		return render(request, 'edit.html', {'form':form})


def order_delete(request, order_id):
	order = Order.objects.get(id=order_id, user=request.user)
	order.delete()
	return redirect('/', messages.success(request, 'Order was successfully deleted.', 'alert-success'))

def chart_ordered_products(user):
	data=[]
	wrapper = {}
	
	orderedItems = OrderItem.objects.filter(order__user = user).values('order__id').annotate(quantity = Count('quantity')).order_by('order__id')
	for row in orderedItems:
		data.append([str(row['order__id']), str(row['quantity'])])
	wrapper['label']='items ordered'
	wrapper['last']='true'
	wrapper['data']=data
	return wrapper

def get_chart_ordered_amounts(user, customer=None):
	data=[]
	wrapper = {}

	orderedItems = OrderItem.objects.filter(order__user = user).filter(order__customer = customer).values('order__id').annotate(total_amount = Sum(F('quantity')*F('price'))).order_by('order__id')
	for row in orderedItems:
		data.append([str(row['order__id']), str(row['total_amount'])])
	wrapper['label']='$'
	wrapper['last']='true'
	wrapper['data']=data
	return wrapper


def order_export(request, customer_id):
	order_resource = OrderResource()
	queryset = Order.objects.filter(customer=customer_id)
	dataset = order_resource.export(queryset)
	response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
	customer = Customer.objects.get(id=customer_id)
	filename = "orders_{}{}".format(customer.first_name, customer.last_name)
	response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(filename)
	return response

def order_single_export(request, order_id):
	item_resource = OrderItemResource()
	queryset = OrderItem.objects.filter(order=order_id)
	dataset = item_resource.export(queryset)
	response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
	order = Order.objects.get(id=order_id)
	customer = Customer.objects.get(id=order.customer.id)
	filename = "order_{}{}_{}".format(customer.first_name, customer.last_name, order.id)
	response['Content-Disposition'] = 'attachment; filename="{}.xls"'.format(filename)
	return response

def supplierorder_list(request):
	if not request.user.is_authenticated:
		return redirect('users:login')
	objs = SupplierOrder.objects.filter(user=request.user)
	args = {
		'title': 'Supplier Order',
		'formset_title': 'Order items',
		'link_new': 'orders:supplierorder_new',
		'link_edit': 'orders:supplierorder_edit',
		'link_delete': 'orders:supplierorder_delete',
		'fields': ['supplier', 'customer', 'first_name', 'last_name', 'phone', 'address'],
		'objs': objs,
		'no_objects_msg': 'You have no Supplier Orders',
		}
	return render(request, 'shop/sheet.html', args)

def supplierorder_new(request):
	if not request.user.is_authenticated:
		return redirect('users:login')
	SupplierOrderFormSet = modelformset_factory(
		SupplierOrderItem, 
		fields=('product', 'price', 'quantity', 'um'), 
		can_delete=True,
		extra=1)
	if request.method == "POST":
		form = SupplierOrderForm(request.POST)
		formset = SupplierOrderFormSet(request.POST, request.FILES)
		if form.is_valid() and formset.is_valid() :
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			instances = formset.save(commit=False)
			for instance in instances:
				instance.order = obj
				instance.save()
			formset.save(commit=True)
			return redirect('orders:supplierorder_list')
	else:
		form = SupplierOrderForm()
		formset = SupplierOrderFormSet(queryset=SupplierOrderItem.objects.none())

	form.fields['supplier'].queryset = Supplier.objects.filter(user=request.user)
	form.fields['customer'].queryset = Customer.objects.filter(user=request.user)
	form.fields['supplier'].empty_label = 'Select a supplier'
	form.fields['customer'].empty_label = 'Select a customer'
	args = {
		'form_title': 'Supplier Order',
		'formset_title': 'Order items',
		'link_new': 'orders:supplierorder_new',
		'link_edit': 'orders:supplierorder_edit',
		'link_delete': 'orders:supplierorder_delete',
		'form': form,
		'formset': formset,
		'filter_portfolio': 1,
		}
	return render(request, 'shop/form_formset_edit.html', args)

def supplierorder_edit(request, pk):
	if not request.user.is_authenticated:
		return redirect('users:login')
	obj = get_object_or_404(SupplierOrder, pk=pk)
	SupplierOrderFormSet = modelformset_factory(
		SupplierOrderItem, 
		fields=('product', 'price', 'quantity', 'um'), 
		extra=1)
	if request.method == "POST":
		form = SupplierOrderForm(request.POST, instance=obj)
		formset = SupplierOrderFormSet(request.POST, request.FILES, queryset=SupplierOrderItem.objects.filter(order=obj))
		if form.is_valid() and formset.is_valid() :
			obj = form.save(commit=False)
			obj.user = request.user
			obj.save()
			instances = formset.save(commit=False)
			for instance in instances:
				instance.order = obj
				instance.save()
			formset.save(commit=True)
			return redirect('orders:supplierorder_list')
	else:
		form = SupplierOrderForm(instance=obj)
		formset = SupplierOrderFormSet(queryset=SupplierOrderItem.objects.filter(order=obj))

# 	form.fields['supplier'].queryset = Supplier.objects.filter(user=request.user)
# 	form.fields['customer'].queryset = Customer.objects.filter(user=request.user)
# 	form.fields['supplier'].empty_label = 'Select a supplier'
# 	form.fields['customer'].empty_label = 'Select a customer'
	form.fields['supplier'].disabled = True
	form.fields['customer'].disabled = True
	for xform in formset:
		xform.fields['product'].queryset=Product.objects.filter(supplier=obj.supplier)
		xform.fields['price'].disabled=True
	args = {
		'form_title': 'Supplier Order',
		'formset_title': 'Order items',
		'link_new': 'orders:supplierorder_new',
		'link_edit': 'orders:supplierorder_edit',
		'link_delete': 'orders:supplierorder_delete',
		'form': form,
		'formset': formset,
		'filter_portfolio': 2,
		}
	return render(request, 'shop/form_formset_edit.html', args)

def supplierorder_delete(request, pk):
	obj = get_object_or_404(SupplierOrder, pk=pk)
	obj.delete()
	return redirect('orders:supplierorder_list')