from django.db import models
from shop.models import Product, Supplier, UnitMeasure
from users.models import Profile
from decimal import Decimal

class Portfolio(models.Model):
	name = models.CharField(max_length=30)
	user = models.ForeignKey(Profile, related_name='portfolios')
	supplier = models.ForeignKey(Supplier, related_name='porfolios')

	class Meta:
		ordering = ('supplier',)
		verbose_name = 'portfolio'
		verbose_name_plural = 'portfolios'

	def __str__(self):
		return "{} {}".format(self.supplier.name, self.id)

	def get_cost(self):
		products = PortfolioProduct.objects.filter(portfolio=self)
	
		return sum((Decimal(product.product.price) * product.quantity) for product in products)



class PortfolioProduct(models.Model):
	portfolio = models.ForeignKey(Portfolio, related_name='products')
	product = models.ForeignKey(Product, related_name='product_porfolios')
	quantity = models.PositiveIntegerField(default=1)
	um = models.ForeignKey(UnitMeasure, related_name='protfolio_products')

	def get_total_cost(self):
		return self.quantity * self.product.price