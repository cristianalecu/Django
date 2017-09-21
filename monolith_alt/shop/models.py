from django.db import models
from django.core.urlresolvers import reverse
from users.models import Profile
from django.contrib.auth.models import User

class Category(models.Model):
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	
	class Meta:
		ordering = ('name',)
		verbose_name = 'category'
		verbose_name_plural = 'categories'
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_criteria', args=[self.slug])

class Supplier(models.Model):
	user = models.ForeignKey(User, blank=True, null=True)
	name = models.CharField(max_length=100, db_index=True)
	address = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True, unique=True)
	
	class Meta:
		ordering = ('name', 'address',)
		verbose_name = 'supplier'
		verbose_name_plural = 'suppliers'
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_list_by_criteria', args=[self.slug])

class UnitMeasure(models.Model):
	name = models.CharField(max_length=100, db_index=True)

class Product(models.Model):
	category = models.ForeignKey(Category, related_name='products')
	supplier = models.ForeignKey(Supplier, related_name='products')
	name = models.CharField(max_length=200, db_index=True)
	slug = models.SlugField(max_length=200, db_index=True)
	image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=10, decimal_places=2)
	stock = models.PositiveIntegerField()
	available = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ('name',)
		index_together = (('id', 'slug'),)
	
	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('shop:product_detail', args=[self.id, self.slug])