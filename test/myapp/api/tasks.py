# tasks/tasks.py

from celery import shared_task
from django.utils import timezone
from .models import Task
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)

@shared_task
def check_task_due_dates():
    tasks = Task.objects.filter(due_date__lte=timezone.now(), is_notified=False)
    logger.info(f"Found {len(tasks)} tasks to notify.")

    for task in tasks:
        logger.info(f"Processing task: {task.title} (ID: {task.id})")
        send_mail(
            subject=f"Задача '{task.title}' наступила",
            message=f"Задача '{task.title}' должна быть выполнена. Описание: {task.description}",
            from_email='prostodima0011@gmail.com',
            recipient_list=[task.user.email],
        )
        task.is_notified = True
        task.save()

    return f"Checked {len(tasks)} tasks."

