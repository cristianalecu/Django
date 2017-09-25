from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^mysupplierorders/$', views.supplierorder_list, name='supplierorder_list'), 
	url(r'^addmysupplierorder/$', views.supplierorder_new, name='supplierorder_new'),
	url(r'^editmysupplierorder/(?P<pk>\d+)/$', views.supplierorder_edit, name='supplierorder_edit'),
	url(r'^delmysupplierorder/(?P<pk>\d+)/$', views.supplierorder_delete, name='supplierorder_delete'),
	url(r'^$', views.order_list, name='order_list'),
	url(r'^(?P<order_id>\d+)/$', views.order_detail, name='order_detail'), 
	url(r'^create/$', views.order_create, name='order_create'),
	# url(r'^edit/(?P<order_id>\d+)/$', views.order_edit, name='order_edit'),
	url(r'^delete/(?P<order_id>\d+)/$', views.order_delete, name='order_delete'),
	url(r'^export/(?P<customer_id>\d+)/$', views.order_export, name='order_export'),
	url(r'^export/order/(?P<order_id>\d+)/$', views.order_single_export, name='order_single_export'),

]