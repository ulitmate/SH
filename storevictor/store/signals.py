from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OperatorChat, Schedule, Discount
from .tasks import send_notification_email_task

import datetime
import pytz


@receiver(post_save, sender=OperatorChat)
def create_schedule(sender, instance, created, **kwargs):

    '''
        Signal function to auto-create a record/chat to schedule to be sent at an 
        appropriate time, considring time-zone of shop so operators could respond 
        on a work schedule.

        It's assumed that operator and shop are on the same time-zone
    '''

    if created:
        timezone_of_store = pytz.timezone(instance.conversation_party.store.timezone)

        now = datetime.datetime.now()
        date_string = now.strftime("%Y-%m-%d")
        datetime_format = "%Y-%m-%d %H:%M:%S"
        low_ref_datetime_string = date_string + " " + "09:00:00"
        upper_ref_datetime_string = date_string + " " + "21:00:00"
        low_ref_datetime_object = datetime.datetime.strptime(low_ref_datetime_string, datetime_format)
        upper_ref_datetime_object = datetime.datetime.strptime(upper_ref_datetime_string, datetime_format)

        low_ref_datetime_object = low_ref_datetime_object.replace(tzinfo=timezone_of_store)
        upper_ref_datetime_object = upper_ref_datetime_object.replace(tzinfo=timezone_of_store)

        last_entry = Schedule.objects.filter(sending_datetime__gte=datetime.datetime.now()).order_by('sending_datetime').last()


        
        interval = (60.0/90.0) * 60.0
        interval = 10
        
        if not last_entry:
            sending_datetime = datetime.datetime.now().replace(tzinfo=timezone_of_store)
        else:   
            sending_datetime = last_entry.sending_datetime + datetime.timedelta(minutes=interval)
        
        if sending_datetime < low_ref_datetime_object or sending_datetime > upper_ref_datetime_object:
            sending_datetime = low_ref_datetime_object + datetime.timedelta(days=1)
        
        
        schedule = Schedule.objects.create(chat = instance, sending_datetime=sending_datetime)

        discount_code = Discount.objects.get(store=instance.conversation_party.store).code
        

        subject = "RE: Celery Check"
        send_notification_email_task.delay(
                    schedule = schedule.sending_datetime, 
                    subject = subject, 
                    body = instance.message, 
                    discount_code = discount_code,
                    client_name = instance.chat.user.first_name, 
                    operator_first_name=instance.operator.user.get_full_name(),
                    dest_email=instance.chat.user.email
                    )

