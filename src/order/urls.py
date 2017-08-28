from django.conf.urls import url

urlpatterns = [
    # ex: /polls/
    url(r'^$', include('admin/order')),

]