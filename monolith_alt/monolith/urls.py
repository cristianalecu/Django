from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth

from shop import views

urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^orders/', include('orders.urls', namespace='orders')),
	url(r'^cart/', include('cart.urls', namespace='cart')),
	url(r'^products/', include('shop.urls', namespace='shop')),
	url(r'^portfolios/', include('portfolios.urls', namespace='portfolios')),
	url(r'^login/', auth.login, {'template_name': 'users/login.html'}, name="login"),
	url(r'^$', views.dashboard, name='dashboard'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)