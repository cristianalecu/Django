
from django.http import HttpResponseRedirect
from django.core import urlresolvers

def home(request):
    return HttpResponseRedirect(urlresolvers.reverse('admin:app_list', args=("order",)))
