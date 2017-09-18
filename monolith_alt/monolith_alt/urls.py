"""monolith_alt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth

from shop import views

from rest_framework import routers
from rest_export.views import CategoryViewSet, SupplierViewSet, UnitMeasureViewSet, ProductViewSet
from rest_export.views import ProfileViewSet, CustomerViewSet, OrderViewSet, OrderItemViewSet, UserViewSet, GroupViewSet

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'unitmeasures', UnitMeasureViewSet)
router.register(r'products', ProductViewSet)
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'profiles', ProfileViewSet)
router.register(r'customers', CustomerViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'orderitems', OrderItemViewSet)

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^orders/', include('orders.urls', namespace='orders')),
	url(r'^cart/', include('cart.urls', namespace='cart')),
	url(r'^products/', include('shop.urls', namespace='shop')),
	url(r'^portfolios/', include('portfolios.urls', namespace='portfolios')),
	url(r'^login/', auth.login, {'template_name': 'users/login.html'}, name="login"),
	url(r'^$', views.dashboard, name='dashboard'),
    url(r'^restf/get/', include(router.urls)), 
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
