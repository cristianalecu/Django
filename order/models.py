from django.db import models
from django.utils import timezone


class Order(models.Model):
    author = models.ForeignKey('auth.User')
    comments = models.TextField()
    #status = options.SmallIntegerField()
    status = models.PositiveIntegerField()
    total = models.DecimalField(decimal_places=2,max_digits=10)


    def __str__(self):
        return self.id
