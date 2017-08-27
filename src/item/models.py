from django.db import models
from django.utils import timezone


class Item(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10)
    image = models.ImageField()
    price_type = ('Piece', 'weight', 'Length', 'Square meter', 'Cube meter')

    def __str__(self):
        return self.title
