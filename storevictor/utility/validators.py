from django.utils import timezone
from django.core.exceptions import ValidationError
import datetime
from phonenumber_field.phonenumber import to_python
from phonenumbers.phonenumberutil import is_possible_number
from phonenumber_field.modelfields import PhoneNumber, PhoneNumberField
from .error_codes import AccountErrorCode

# Create your validation tools here.

def validate_possible_number(phone, country=None):
    phone_number = to_python(phone, country)
    if (
        phone_number
        and not is_possible_number(phone_number)
        or not phone_number.is_valid()
    ):
        raise ValidationError(
            "The phone number entered is not valid.", code=AccountErrorCode.INVALID
        )
    return phone_number

class PossiblePhoneNumberField(PhoneNumberField):
    """Less strict field for phone numbers written to database."""

    default_validators = [validate_possible_number]


def no_future(value):

    # Check for a datetime.datetime object 
    if isinstance(value, datetime.datetime):
        if value > timezone.now():
            raise ValidationError('Date cannot be in the future.')
    else:
        if value > timezone.now().date():
            raise ValidationError('Date cannot be in the future.')

def no_past(value):
    
    # Check for a datetime.datetime object 
    if isinstance(value, datetime.datetime):
        if value < timezone.now():
            raise ValidationError('Date cannot be in the past.')
    else:
        if value < timezone.now().date():
            raise ValidationError('Date cannot be in the past.')
