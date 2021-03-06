from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^mines/$', views.customer_portfolio_list, name='customer_portfolio_list'), 
	url(r'^addmine/$', views.customer_portfolio_new, name='customer_portfolio_new'),
	url(r'^editmine/(?P<pk>\d+)/$', views.customer_portfolio_edit, name='customer_portfolio_edit'),
	url(r'^delmine/(?P<pk>\d+)/$', views.customer_portfolio_delete, name='customer_portfolio_delete'),
	url(r'^get_portfolio_products/(?P<customer_id>\d+)/(?P<supplier_id>\d+)/$',	views.get_portfolio_products, name='get_portfolio_products'),
	url(r'^list/$', views.portfolio_list, name='portfolio_list'),
	url(r'^add/$', views.portfolio_add, name='portfolio_add'),
	url(r'^order/$', views.portfolio_order, name='portfolio_order'),
	url(r'^(?P<id>\d+)/$', views.portfolio_detail, name='portfolio_detail'),
	url(r'^delete/(?P<portfolio_id>\d+)/$', views.portfolio_delete, name='portfolio_delete'),
]