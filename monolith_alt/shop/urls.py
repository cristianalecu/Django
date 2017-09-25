from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^get-products/(?P<supplier_id>\d+)/$',	views.get_products, name='get-products'),
	url(r'^product-autocomplete/$',	views.ProductAutocomplete.as_view(), name='product-autocomplete'),
	url(r'^supplier-autocomplete/$', views.SupplierAutocomplete.as_view(), name='supplier-autocomplete'),
	url(r'^products/import/$', views.product_import, name='product_import'),
	url(r'^$', views.product_list, name='product_list'),
	url(r'^(?P<criteria_slug>[-\w]+)/$', views.product_list, name='product_list_by_criteria'),
	url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]