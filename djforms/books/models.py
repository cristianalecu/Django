from django.db import models
from django.contrib.auth.models import User

TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
)

class Author(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    title = models.CharField(max_length=3, choices=TITLE_CHOICES)
    birth_date = models.DateField(blank=True, null=True)

    def __str__(self):              # __unicode__ on Python 2
        return self.name

class Book(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author)
    due_date = models.DateField(blank=False, null=False)

