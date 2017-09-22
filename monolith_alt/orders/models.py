from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from users.models import Customer, Salesperson
from shop.models import Product, Supplier, UnitMeasure
from decimal import Decimal

class Order(models.Model):
	user = models.ForeignKey(User, related_name='orders')
	customer = models.ForeignKey(Customer, related_name='orders')
	# salesperson = models.ForeignKey(Salesperson, related_name='orders')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	
	# supplier = models.ForeignKey(Supplier, related_name='orders')
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	paid = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('-created',)
	
	def __str__(self):
		return 'Order {}'.format(self.id)
	
	def get_total_cost(self):
		total_cost = sum(item.get_cost() for item in self.items.all())
		return total_cost

class SupplierOrder(models.Model):
	user = models.ForeignKey(User, related_name='supplier_orders')
	customer = models.ForeignKey(Customer, related_name='supplier_orders')
	supplier = models.ForeignKey(Supplier, related_name='supplier_orders')
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	email = models.EmailField()
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)	
	notes = models.CharField(max_length=250)
	created = models.DateTimeField(auto_now_add=True)
	status = models.BooleanField(default=False)

class SupplierOrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='supplier_order_items')
	product = models.ForeignKey(Product, related_name='supplier_order_products')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	um = models.ForeignKey(UnitMeasure, related_name='supplier_order_products')

	def __str__(self):
		return '{}'.format(self.id)
	
	def get_cost(self):
		return self.price * self.quantity
	
	
class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items')
	product = models.ForeignKey(Product, related_name='order')
	price = models.DecimalField(max_digits=10, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	um = models.ForeignKey(UnitMeasure, related_name='products')

	def __str__(self):
		return '{}'.format(self.id)
	
	def get_cost(self):
		return self.price * self.quantity