from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from order import views
 
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^blog/', include('blog.urls')),
    #url(r'^', include('orders.urls')),
    url(r'^$', views.home, name='home'),
 ]