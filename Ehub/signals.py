from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .models import Customer
'''
def customer_profile(sender, instance, created, **kwargs):
	if created:
		group = Group.objects.get(name='Customers')
		instance.groups.add(group)  
		Customer.objects.create(
			user=instance,
			email=instance.email
			)
		print('Customer obj created for Registered User!')

post_save.connect(customer_profile, sender=User)
'''