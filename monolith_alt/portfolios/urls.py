from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.portfolio_list, name='portfolio_list'),
	url(r'^add/$', views.portfolio_add, name='portfolio_add'),
	url(r'^order/$', views.portfolio_order, name='portfolio_order'),
	url(r'^(?P<id>\d+)/$', views.portfolio_detail, name='portfolio_detail'),
	url(r'^delete/(?P<portfolio_id>\d+)/$', views.portfolio_delete, name='portfolio_delete'),
]