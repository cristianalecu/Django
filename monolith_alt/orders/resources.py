from import_export import resources, fields
from .models import Order, OrderItem

class OrderResource(resources.ModelResource):
	total_cost = fields.Field()

	class Meta:
		model = Order
		fields = ('id', 'first_name', 'last_name', 'email', 'address', 'phone', 'total_cost')
		export_order = ('id', 'first_name', 'last_name', 'email', 'address', 'phone', 'total_cost')

	def dehydrate_total_cost(self, order):
		total_cost = order.get_total_cost()
		return "{}".format(total_cost)


class OrderItemResource(resources.ModelResource):
	cost = fields.Field()
	product = fields.Field()
	um = fields.Field()
	class Meta:
		model = OrderItem
		fields = ('product', 'price', 'quantity', 'um')
		export_order = ('product', 'price', 'quantity', 'um')

	def dehydrate_cost(self, order_item):
		cost = order_item.get_cost()
		return "{}".format(cost)

	def dehydrate_product(self, order_item):
		product = order_item.product.name
		return "{}".format(product)

	def dehydrate_um(self, order_item):
		um = order_item.um.name
		return um