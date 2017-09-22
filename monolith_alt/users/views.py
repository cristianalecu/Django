from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Q
from django.contrib import messages
from django.http import HttpResponse
from django.core import serializers
from dal import autocomplete
from tablib import Dataset

from django.forms import modelformset_factory
from orders.views import get_orders_of_user, get_chart_ordered_amounts
from shop.models import Product, Supplier

from .forms import SignUpForm, CustomerForm
from .models import Customer, Profile
from .resources import CustomerResource
from django.template.defaultfilters import slugify

def signup(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.refresh_from_db()  # load the profile instance created by the signal
			user.profile.email = form.cleaned_data.get('email')
			user.profile.first_name = form.cleaned_data.get('first_name')
			user.profile.last_name = form.cleaned_data.get('last_name')
			user.profile.address = form.cleaned_data.get('address')
			user.profile.city = form.cleaned_data.get('city')
			user.profile.phone = form.cleaned_data.get('phone')
			user.save()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=user.username, password=raw_password)
			login(request, user)
			return redirect('/')
	else:
		form = SignUpForm()
	return render(request, 'users/signup.html', {'form': form})


def get_favorite_products(user):
	if not user.is_anonymous:
		favorites = Product.objects.annotate(qty=Sum('product__quantity')).order_by('-qty')[:5]
		# favorites = Product.objects.filter(product__user=user.profile)
	else:
		favorites = None

	return favorites

def customer_list(request):
	if request.user.is_authenticated:
		customers = Customer.objects.filter(user=request.user)
		customer_form = CustomerForm()
		from_add = request.session.pop('from_add', False)
		if from_add:
			customer_form.initial['first_name'] = request.session.pop('first_name', "")
			customer_form.initial['last_name'] = request.session.pop('last_name', "")
			customer_form.initial['address'] = request.session.pop('address', "")
			customer_form.initial['city'] = request.session.pop('city', "")
			customer_form.initial['phone'] = request.session.pop('phone', "")
			customer_form.initial['email'] = request.session.pop('email', "")
		
	context = {
		'customers': customers,
		'customer_form': customer_form,
	}
	return render(request, 'users/customer/list.html', context)

def customer_sheet(request):
	CustomersFormSet = modelformset_factory(
		 Customer, 
		 fields=('first_name','last_name','address','city','phone','email'), 
		 can_delete=True,
		 can_order=True,
		 extra=1)
	if not request.user.is_authenticated:
		return redirect('users:login')
		
	if request.method == "POST":
		formset = CustomersFormSet(request.POST)
		if formset.is_valid() :
			instances = formset.save(commit=False)
			for instance in instances:
				instance.user = request.user
				
				if instance.profile_id:
					instance.profile.user = request.user
					instance.profile.user_type = 2   #Customer
					instance.profile.address = instance.address
					instance.profile.phone = instance.phone
					instance.profile.save()
				else :
					pro =get_object_or_404(Profile, pk=request.user.id)
					if not pro:
						pro = Profile.objects.create(user=request.user, user_type=2, address= instance.address, phone= instance.phone, created='2010-01-01')
						pro.save()
					instance.profile = pro
					instance.profile.save()
					instance.profile_id = instance.profile.id
				instance.save()
			formset.save()   # commit
			return redirect('users:customer_sheet')
	else:
		formset = CustomersFormSet(queryset=Customer.objects.filter(user=request.user))
	 
	return render(request, 'users/customer/sheet.html', {'title': 'My Customers', 'formset': formset})

def supplier_sheet(request):
	SuppliersFormSet = modelformset_factory(
		 Supplier, 
		 fields=('name','address'), 
		 can_delete=True,
		 can_order=True,
		 extra=1)
	if not request.user.is_authenticated:
		return redirect('users:login')
		
	if request.method == "POST":
		formset = SuppliersFormSet(request.POST)
		if formset.is_valid() :
			instances = formset.save(commit=False)
			for instance in instances:
				instance.user = request.user
				instance.slug = slugify(instance.name)
				instance.save()
			formset.save()   # commit
			return redirect('users:supplier_sheet')
	else:
		formset = SuppliersFormSet(queryset=Supplier.objects.filter(user=request.user))
	 
	return render(request, 'users/customer/sheet.html', {'title': 'My Suppliers', 'formset': formset}, )

def customer_detail(request, id):
	customer = None

	if request.user.is_authenticated:
		customer = get_object_or_404(Customer, id=id)
		if customer:
			orders_of_customer = get_orders_of_user(request.user, customer)
			chart_amount = get_chart_ordered_amounts(request.user, customer)
	return render(request, 'users/customer/detail.html', {'customer': customer, 'orders':orders_of_customer, 'chart_amount':chart_amount})


def customer_add(request):
	if request.user.is_authenticated:
		if request.method == 'POST':
			customer_form = CustomerForm(request.POST)

			if customer_form.is_valid():
				customer = customer_form.save(commit=False)
				customer.user = request.user
				customer.save()
				messages.success(request, 'Customer added succesfully!', 'alert-success')
			else:
				err = ""
				for key, error in customer_form.errors.items():
					err = err.join(error)
				print(err)
				messages.error(request, "Error saving customer! " + err, 'alert-danger')
				request.session['from_add'] = True
				request.session['first_name'] = customer_form.cleaned_data.get('first_name')
				request.session['last_name'] = customer_form.cleaned_data.get('last_name')
				request.session['address'] = customer_form.cleaned_data.get('address')
				request.session['city'] = customer_form.cleaned_data.get('city')
				request.session['phone'] = customer_form.cleaned_data.get('phone')
				request.session['email'] = customer_form.cleaned_data.get('email')

	return redirect('users:customer_list')

def customer_delete(request, customer_id):
	customer = Customer.objects.get(id=customer_id, user=request.user)
	customer.delete()
	return redirect(request.META.get('HTTP_REFERER'), messages.success(request, "Customer was successfully deleted!", 'alert-success'))


def get_customers(self, customer_id):
	customers = Customer.objects.filter(id=customer_id)
	return HttpResponse(serializers.serialize('json', customers), content_type="application/json")


def customer_import(request):
	context = {}
	if request.method == 'POST':
		customer_resource = CustomerResource()
		dataset = Dataset()
		new_customers_file = request.FILES['customers_file']
		string_file = new_customers_file.read().decode()
		page_result={}
		customers = []
		try:
			imported_data = dataset.load(string_file, format='csv')
			# result = customer_resource.import_data(dataset, dry_run=True)  # Test the data import
			# if not result.has_errors():
			page_result['message']="Success! The following customers were imported:"
			for row in dataset.dict:
				customer = Customer()
				customer.user = request.user
				customer.first_name = row['first_name']
				customer.last_name = row['last_name']
				customer.address = row['address']
				customer.city = row['city']
				customer.phone = row['phone']
				customer.email = row['email']
				customer.save()
				customers.append(customer)
		except Exception:
			page_result['error']="Error while importing customers!"
			# customer_resource.import_data(dataset, dry_run=False)  # Actually import now

		if customers: page_result['customers'] = customers
		context['result'] = page_result
	return render(request, 'users/customer/import.html', context)


class CustomerAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		if not self.request.user.is_authenticated():
			return Customer.objects.none()

		qs = Customer.objects.all()

		if self.q:
			query = Q(first_name__icontains=self.q ) | Q(mast_name__icontains=self.q )
			qs = qs.filter(query)

		return qs