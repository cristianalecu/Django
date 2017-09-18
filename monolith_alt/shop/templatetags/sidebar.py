from django import template
from shop.models import Category, Supplier
register = template.Library()

@register.assignment_tag
def sidebar_categories():
	categories = Category.objects.all()
	return  categories

@register.assignment_tag
def sidebar_suppliers():
	suppliers = Supplier.objects.all()
	return  suppliers