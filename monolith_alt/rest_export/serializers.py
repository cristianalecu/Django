from rest_framework import serializers
from shop.models import Category, Supplier, UnitMeasure, Product
from django.contrib.auth.models import User, Group
from users.models import Profile, Customer
from orders.models import Order, OrderItem

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class SupplierSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Supplier
        fields = ('id', 'name', 'address', 'slug')

class UnitMeasureSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UnitMeasure
        fields = ('id', 'name')

class ProductSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'category', 'supplier', 'name', 'image', 'description', 'price', 'stock', 'available', 'created', 'updated')

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')
        
class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('id', 'user', 'user_type', 'address', 'phone', 'created')

class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ('id', 'profile', 'first_name', 'last_name', 'address', 'city', 'phone', 'email')
        
class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'user', 'customer', 'first_name', 'last_name', 'email', 'address', 'phone', 'paid', 'created', 'updated')

class OrderItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'order', 'product', 'price', 'quantity', 'um')