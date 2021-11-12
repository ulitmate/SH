from django.db.models.signals import post_save
#from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import User
#from store.models import Client


# '''
#     Create Cutomer Account when a user is created
# '''
# @receiver(post_save, sender=User)
# def create_customer(sender, instance, created, **kwargs):
#     if created:
#         Client.objects.create(user = instance)
