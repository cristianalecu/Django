from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from home.forms import HomeForm
from order.models import Item, Order


class HomeView(TemplateView):
    template_name = 'home/home.html'

    def get(self, request):
        form = HomeForm()
        items = Item.objects.all().order_by('-price')
        orders = Order.objects.filter(author=request.user)

        args = {
            'form': form, 'items': items, 'orders': orders
        }
        return render(request, self.template_name, args)

    def post(self, request):
#         form = HomeForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.user = request.user
#             post.save()
# 
#             text = form.cleaned_data['post']
#             form = HomeForm()
#             return redirect('home:home')
# 
#         args = {'form': form, 'text': text}
#         return render(request, self.template_name, args)
        return redirect('home:home')

def add_item(request, operation, pk):
#     friend = User.objects.get(pk=pk)
#     if operation == 'add':
#         Friend.make_friend(request.user, friend)
#     elif operation == 'remove':
#         Friend.lose_friend(request.user, friend)
    return redirect('home:home')
