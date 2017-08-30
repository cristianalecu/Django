import datetime
from django.db import models
from django.utils import timezone

PRICE_TYPE_CHOICES = (
    (1, "Piece"),
    (2, "Weight"),
    (3, "Length"),
    (4, "Square meter"),
    (5, "Cube meter")
)

class Order(models.Model):
    author = models.ForeignKey('auth.User')
    pub_date = models.DateTimeField('date published')
    order_id = models.CharField(max_length=32, editable=False)
    comments = models.TextField()
    #status = options.SmallIntegerField()
    status = models.PositiveIntegerField()
    total = models.DecimalField(decimal_places=2,max_digits=10)

    def __str__(self):
        return self.order_id

    def save(self, *args, **kwargs):
        self.order_id = 'Order ' + str(self.id)
        super(Order, self).save(*args, **kwargs)
        
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    image = models.ImageField(blank=True, null=True)
    price_type = models.IntegerField(choices=PRICE_TYPE_CHOICES, default=1)  


    def __str__(self):
        return self.title

class Orderitem(models.Model):
    item = models.ForeignKey('Item')
    order = models.ForeignKey('Order')
    position = models.IntegerField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    qty = models.DecimalField(decimal_places=3,max_digits=10)

    def __str__(self):
        return self.item.title

