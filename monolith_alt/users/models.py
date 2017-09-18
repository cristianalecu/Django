from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
	USER_TYPE_CHOICES = (
		(0,'Not set'),
		(1,'Staff'),
		(2,'Customer'),
		(3,'Salesperson'),
		)

	user = models.OneToOneField(User, on_delete=models.CASCADE)
	user_type = models.PositiveIntegerField(choices = USER_TYPE_CHOICES, default=0)
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)
	instance.profile.save()

class Customer(models.Model):
	user = models.ForeignKey(User, related_name='customers', blank=True, null=True)
	profile = models.ForeignKey(Profile, related_name='customer', blank=True, null=True)
	first_name = models.CharField(max_length=40)
	last_name = models.CharField(max_length=40)
	address = models.CharField(max_length=250)
	city = models.CharField(max_length=20)
	phone = models.CharField(max_length=20)
	email = email = models.EmailField()

	def __str__(self):
		return self.first_name + " " + self.last_name

class Salesperson(models.Model):
	profile = models.ForeignKey(Profile, related_name='salesperson')
	name = models.CharField(max_length=250)
	address = models.CharField(max_length=250)
	phone = models.CharField(max_length=20)
	email = models.CharField(max_length=250)