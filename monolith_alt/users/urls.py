from django.conf.urls import url
from django.contrib.auth import views as auth
from . import views

urlpatterns = [
	url(r'^login/$', auth.login, {'template_name': 'users/login.html'}, name='login'),
	url(r'^logout/$', auth.logout, {'next_page': '/'}, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^get-customers/(?P<customer_id>\d+)/$',	views.get_customers, name='get-customers'),
  	url(r'^mycustomers/$', views.customer_list, name='customer_list'),
    url(r'^mysuppliers/$', views.supplier_sheet, name='supplier_sheet'),
  	url(r'^customers/$', views.customer_sheet, name='customer_sheet'),
	url(r'^customers/add/$', views.customer_add, name='customer_add'),
	url(r'^customers/(?P<id>\d+)/$', views.customer_detail, name='customer_detail'),
	url(r'^customers/delete/(?P<customer_id>\d+)/$', views.customer_delete, name='customer_delete'),
	url(r'^customers/import/$', views.customer_import, name='customer_import'),
]