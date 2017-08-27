from django.db import models
from django.utils import timezone
from order.models import Order 
from item.models import Item 

class Orderitem(models.Model):
    item = models.ForeignKey('item.Item')
    order = models.ForeignKey('order.Order')
    position = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    qty = models.DecimalField(decimal_places=3,max_digits=10)

    def __str__(self):
        return self.item.title