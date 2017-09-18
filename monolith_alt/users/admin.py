from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import Profile, Customer, Salesperson

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomerInline(admin.StackedInline):
    model = Customer
    can_delete = False
    verbose_name_plural = 'Customer'
    fk_name = 'profile'

class SalespersonInline(admin.StackedInline):
    model = Salesperson
    can_delete = False
    verbose_name_plural = 'Salesperson'
    fk_name = 'profile'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', )
    list_select_related = ('profile', )

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)