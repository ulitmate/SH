from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from utility.validators import no_past, PossiblePhoneNumberField
from utility.models import Address
import uuid
import pytz

# Create your models here.

'''
    Models are built with uuids as foreign-keys and exposed ID.
    MOdels are built with deleted boolean field to toggle and marked as deleted 
    rather than a physical purging of records.
'''


User = get_user_model()
TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class Store(models.Model):

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    name = models.CharField('Store Name', max_length=256, unique=True, blank=True, null=True )
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    telephone =  PossiblePhoneNumberField("Telephone No.", unique=True)
    created_by = models.ForeignKey(User, to_field='uuid', on_delete=models.CASCADE, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.name, self.timezone)

class Discount(models.Model):

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    store = models.ForeignKey(Store, to_field='uuid', on_delete=models.CASCADE, blank=True, null=True)
    code = models.CharField(max_length=12 )
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}-{}'.format(self.store, self.code)


class Client(models.Model):
    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    user = models.ForeignKey(User, to_field="uuid", on_delete=models.CASCADE)
    timezone = models.CharField(max_length=32, choices=TIMEZONES, default='UTC')
    address = models.ManyToManyField(Address, blank=True, null=True)
    #telephone =  PossiblePhoneNumberField("Telephone No.", unique=True)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '{}-{}'.format(self.user, self.timezone)


class Operator(models.Model):

    DEPT_CHOICE = (
        ('sales', 'sales'),
        ('grocery', 'Grocery'),
        ('pharmacy', 'Pharmacy'),
        ('operations', 'Operations'),
    )

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    user = models.ForeignKey(User, to_field="uuid", on_delete=models.CASCADE)
    department = models.CharField(max_length=32, choices=DEPT_CHOICE, default='operations')
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return '{}-{}-{}'.format(self.user, self.store, self.department)


class Conversation(models.Model):
    STATUS_CHOICE = (
        ('pending', 'Pending'),
        ('responding', 'Responding'),
        ('resolved', 'Resolved'),
        ('unresolved', 'Unresolved'),
        
        
    )
    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    store = models.ForeignKey(Store, to_field="uuid", on_delete=models.CASCADE)
    client = models.ForeignKey(Client, to_field="uuid", on_delete=models.CASCADE)
    operator_uuid = models.ForeignKey(Operator, to_field="uuid", on_delete=models.CASCADE)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    resolved_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICE, default='pending')
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}-{}'.format(self.store, self.client)

class ClientChat(models.Model):

    COMM_CHOICE = (
        ('sending', 'sending'),
        ('receiving', 'receiving'),        
    )

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    conversation_party = models.ForeignKey(Conversation, to_field="uuid", on_delete=models.CASCADE)
    communication = models.CharField(max_length=12, choices=COMM_CHOICE, blank=True, null=True)
    user = models.ForeignKey(User, to_field='uuid', on_delete=models.CASCADE, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=32,  default='pending')
    message = models.TextField('Chat Payload',
                                max_length=300,
                                blank=True, 
                                null=True,
                                validators=[
                                RegexValidator(
                                    regex='[\*a-zA-Z0-9_\{\}\$\%\_\-\\\\\/\~\@\#\$\%\^\&\*\(\)\!\?]*',
                                    message='Please ensure that you use right characters in your message',
                                    code='invalid_username'
                                    ),
                                ]
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.conversation_party.uuid)


class OperatorChat(models.Model):

    COMM_CHOICE = (
        ('sending', 'sending'),
        ('receiving', 'receiving'),        
    )

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    conversation_party = models.ForeignKey(Conversation, to_field="uuid", on_delete=models.CASCADE)
    operator = models.ForeignKey(Operator, to_field='uuid', on_delete=models.CASCADE, blank=True, null=True)
    chat = models.ForeignKey(ClientChat, to_field='uuid', on_delete=models.CASCADE, blank=True, null=True)
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=32,  default='pending')
    message = models.TextField('Chat Payload',
                                max_length=300,
                                blank=True, 
                                null=True,
                                validators=[
                                RegexValidator(
                                    regex='[\*a-zA-Z0-9_\{\}\$\%\_\-\\\\\/\~\@\#\$\%\^\&\*\(\)\!\?]*',
                                    message='Please ensure that you use right characters in your message',
                                    code='invalid_username'
                                    ),
                                ]
    )
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.chat)

class Schedule(models.Model):

    STATUS_CHOICE = (
        ('sent', 'sent'),
        ('pending', 'pending')        
    )

    uuid = models.CharField(default=uuid.uuid4, max_length=40, editable=False, unique=True)
    chat = models.ForeignKey(OperatorChat, to_field="uuid", on_delete=models.CASCADE)
    sending_datetime = models.DateTimeField()
    created_datetime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    status = models.CharField(max_length=32, choices=STATUS_CHOICE,  default='pending')

    def __str__(self):
        return '{}-{}'.format(self.chat, self.sending_datetime)

   