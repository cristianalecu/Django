from rest_framework import viewsets
from shop.models import Category, Supplier, UnitMeasure, Product
from django.contrib.auth.models import User, Group
from users.models import Profile, Customer
from orders.models import Order, OrderItem
from rest_export.serializers import CategorySerializer, SupplierSerializer, UnitMeasureSerializer, ProductSerializer
from rest_export.serializers import ProfileSerializer, CustomerSerializer, OrderSerializer, OrderItemSerializer, UserSerializer, GroupSerializer
from rest_export.permissions import CanModifyOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Categoryes to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class SupplierViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Suppliers to be viewed or edited.
    """
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class UnitMeasureViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows UnitMeasures to be viewed or edited.
    """
    queryset = UnitMeasure.objects.all()
    serializer_class = UnitMeasureSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ProfileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Profiles to be viewed or edited.
    """
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows  Customers to be viewed or edited.
    """
    queryset =  Customer.objects.all()
    serializer_class =  CustomerSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Orders to be viewed or edited.
    """
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )

class OrderItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Products to be viewed or edited.
    """
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
        
    permission_classes = (
        CanModifyOrReadOnly,
        )
