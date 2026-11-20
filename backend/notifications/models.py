
from django.conf import settings
from django.db import models


class Notification(models.Model):

    class NotificationType(models.TextChoices):
        TASK_ASSIGNED = 'TASK_ASSIGNED', 'Task Assigned'
        TASK_UPDATED = 'TASK_UPDATED', 'Task Updated'
        PROJECT_UPDATE = 'PROJECT_UPDATE', 'Project Update'
        MILESTONE_UPDATE = 'MILESTONE_UPDATE', 'Milestone Update'
        RISK_UPDATE = 'RISK_UPDATE', 'Risk Update'
        SYSTEM = 'SYSTEM', 'System Notification'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(max_length=200)

    message = models.TextField()

    notification_type = models.CharField(
        max_length=30,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )

    is_read = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.recipient.username}"
