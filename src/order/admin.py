from django.contrib import admin
from .models import Order
from .models import Item
from .models import Orderitem

class OrderItemsInline(admin.TabularInline):
    model = Orderitem
    extra = 3
    
class OrderAdmin(admin.ModelAdmin):
    fieldsets = [
        (None              , {'fields': ['author']}),
        (None              , {'fields': ['comments']}),
        (None              , {'fields': ['status']}),
        (None              , {'fields': ['total']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [OrderItemsInline]
    list_display = ('order_id', 'author', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    
class ItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'description')
    list_filter = ['price', 'price_type']
    search_fields = ['title']

admin.site.register(Item, ItemAdmin)
admin.site.register(Order, OrderAdmin)


