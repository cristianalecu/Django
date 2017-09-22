from django.contrib import admin
from portfolios.models import CustomerPortfolio, CustomerPortfolioProduct

class CustomerPortfolioProductsInline(admin.TabularInline):
    model = CustomerPortfolioProduct
    extra = 3
    
class CustomerPortfolioAdmin(admin.ModelAdmin):
    fieldsets = [
        (None              , {'fields': ['name']}),
        (None              , {'fields': ['user']}),
        (None              , {'fields': ['supplier']}),
        (None              , {'fields': ['customer']}),
    ]
    inlines = [CustomerPortfolioProductsInline]
    list_display = ('name', 'user', 'supplier', 'customer')
    list_filter = ['user']
    search_fields = ['name']
    
admin.site.register(CustomerPortfolio, CustomerPortfolioAdmin)
admin.site.register(CustomerPortfolioProduct)