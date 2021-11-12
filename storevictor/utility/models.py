from django.db import models
from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone


# Create your models here.
User = get_user_model()

class Address(models.Model):
    PLACE_CHOICE = ( ('residence', 'Residence'),
		('work-place', 'Work-Place'))

    place = models.CharField('Residence or Work-Place', max_length=100, choices=PLACE_CHOICE)
    apartment_house_no = models.CharField('House or Apt No.', max_length=100)
    street_Address = models.CharField('Street Name and/or Number', max_length=100)
    surburb = models.CharField('Surburb', max_length=100)
    city = models.CharField('City', max_length=100)
    zip = models.CharField('Zip', help_text='Enter Your Residential GH-POST GPS or Zip Code', max_length=100, blank=True)
    country = CountryField() 
    date_posted = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.zip:
            return '{}-{}'.format(self.street_Address, self.zip)
        else:
            return '{}-{}'.format(self.street_Address, self.surburb)



