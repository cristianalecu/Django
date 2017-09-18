from import_export import resources, fields
from .models import Customer

class CustomerResource(resources.ModelResource):
	class Meta:
		model = Customer
		fields = ('id','first_name', 'last_name', 'address', 'city', 'phone', 'email',)
