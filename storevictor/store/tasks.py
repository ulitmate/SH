from celery.decorators import task
from celery.utils.log import get_task_logger
from .notifications import notification


logger = get_task_logger(__name__)


@task(name="send_notification_email_task")
def send_notification_email_task(schedule, subject, body, discount_code, client_name,  operator_first_name, dest_email):
    
    '''
        Celery task to handle mail sending based on ETA from Schedule Table/Model
    '''

    execution_time = schedule.sending_datetime
    
    logger.info("Sent chat to client")
    schedule.status = "sent"
    schedule.save()
    return notification(subject, body, discount_code, client_name,  operator_first_name, dest_email).apply_async(eta=execution_time)

