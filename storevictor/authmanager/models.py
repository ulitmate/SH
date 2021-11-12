from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from utility.validators import no_past, PossiblePhoneNumberField
from PIL import Image 
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
import uuid


# Create your models here.
class UserManager(BaseUserManager):
	def create_user(self, email, first_name, last_name, other_names, telephone, title, password=None, is_active=True, staff=False, admin=False):
		if not email:
			raise ValueError("User must have an email address")
		if not password:
			raise ValueError("User must have a password")

		user_obj = self.model(email = self.normalize_email(email))
		user_obj.set_password(password) # change user password
		user_obj.staff = staff
		user_obj.admin = admin
		user_obj.is_active = is_active
		user_obj.first_name = first_name
		user_obj.last_name = last_name
		user_obj.other_names = other_names
		user_obj.telephone = telephone
		user_obj.title = title

		user_obj.save(using=self._db)

		return user_obj

	def create_Staffuser(self, email, first_name, last_name, other_names, telephone, title, password=None):
		user = self.create_user(
			email, first_name, last_name, other_names, telephone, title, password=password, staff=True)
		return user

	def create_superuser(self, email, first_name, last_name, other_names, telephone, password=None):

		user = self.create_user(email, first_name, last_name, other_names, telephone, title=None, password=password, staff=True, admin=True)

		return user


class User(AbstractBaseUser):
    GENDER_CHOICE = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    title = models.CharField(max_length=12, blank=True, null=True)
    email = models.EmailField(help_text='Enter your email address.', max_length=255, unique=True)
    first_name = models.CharField(help_text='Enter your first name.', max_length=255)
    last_name = models.CharField(help_text='Enter your Last or Surname only.', max_length=255)
    other_names = models.CharField(help_text='Enter your middle name(s).', max_length=255, blank=True, null=True)
    telephone =  PossiblePhoneNumberField("Telephone No.", unique=True)
    date_of_birth = models.DateField('Date of Birth', blank=True, null=True)
    gender = models.CharField(help_text='Enter middle or other names.', choices=GENDER_CHOICE, max_length=255)
    #history = audit.AuditTrail()

    username = None

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name', 'other_names', 'telephone']

    objects = UserManager()

    def __str__(self):
        return '{} {} {}'.format(self.title, self.first_name, self.last_name)

    def get_full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

    def get_full_name_with_title(self):
        return '{} {} {}'.format(self.title, self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_staff(self):
        return self.staff

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')