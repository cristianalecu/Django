from django import template
from orders.views import order_list as ol
from orders.models import Order
register = template.Library()

# @register.assignment_tag
# def chart_ordered_products():
# 	# categories = Category.objects.all()
# 	query = Order.objects.all()
# 	for row in query:
# 	    data.append([str(row.time), str(row.rate)])

# 	data = ['label': 'Pageviews', 'last': 'true']
# 	data = json.dumps(data, cls=DjangoJSONEncoder)
# 	return data "{label: 'Pageviews',data: [[1, 1100],[2, 2450],[3, 3800],[4, 3400],[5, 3000],[6, 5250],[7, 7500],[8, 5500],[9, 3500],[10, 4000],[11, 4500],[12, 3000]],last: true}"

@register.inclusion_tag('orders/list_naked.html', takes_context=True)
def order_list(context):
	request = context['request']
	return {'content':ol(request, True).content.decode("utf-8")}

# @register.inclusion_tag('orders/list_naked.html', takes_context=True)
# def favorite products(context):
# 	request = context['request']
# 	return {'content':ol(request, True).content.decode("utf-8")}