from django.conf import settings
from django.db import models


class Project(models.Model):

    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'Planning'
        ACTIVE = 'ACTIVE', 'Active'
        ON_HOLD = 'ON_HOLD', 'On Hold'
        COMPLETED = 'COMPLETED', 'Completed'

    name = models.CharField(max_length=200)

    description = models.TextField()

    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='managed_projects'
    )

    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='joined_projects',
        blank=True
    )

    start_date = models.DateField()

    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Milestone(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        IN_PROGRESS = 'IN_PROGRESS', 'In Progress'
        COMPLETED = 'COMPLETED', 'Completed'

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='milestones'
    )

    title = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    due_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.project.name}"