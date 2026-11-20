
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from tasks.models import Task
from .models import Notification


@receiver(pre_save, sender=Task)
def store_previous_task_values(sender, instance, **kwargs):
    """
    Store previous task values before updating a task.
    """

    if instance.pk:
        try:
            old_task = Task.objects.get(pk=instance.pk)

            instance._old_assigned_to_id = old_task.assigned_to_id
            instance._old_status = old_task.status

        except Task.DoesNotExist:
            instance._old_assigned_to_id = None
            instance._old_status = None

    else:
        instance._old_assigned_to_id = None
        instance._old_status = None


@receiver(post_save, sender=Task)
def create_task_notifications(sender, instance, created, **kwargs):

    # Notification when a task is newly assigned
    if created and instance.assigned_to:

        Notification.objects.create(
            recipient=instance.assigned_to,
            title="New Task Assigned",
            message=f"You have been assigned a new task: {instance.title}",
            notification_type=Notification.NotificationType.TASK_ASSIGNED
        )

    # Notification when task is reassigned
    elif (
        not created
        and instance.assigned_to
        and instance._old_assigned_to_id != instance.assigned_to_id
    ):

        Notification.objects.create(
            recipient=instance.assigned_to,
            title="Task Assigned to You",
            message=f"A task has been assigned to you: {instance.title}",
            notification_type=Notification.NotificationType.TASK_ASSIGNED
        )

    # Notification when task status changes
    if (
        not created
        and instance._old_status is not None
        and instance._old_status != instance.status
    ):

        Notification.objects.create(
            recipient=instance.created_by,
            title="Task Status Updated",
            message=(
                f"The status of task '{instance.title}' "
                f"has changed to {instance.get_status_display()}."
            ),
            notification_type=Notification.NotificationType.TASK_UPDATED
        )
