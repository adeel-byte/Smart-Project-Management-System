
from django.conf import settings
from django.db import models


class Risk(models.Model):

    class Category(models.TextChoices):
        TECHNICAL = 'TECHNICAL', 'Technical Risk'
        PROJECT = 'PROJECT', 'Project Risk'
        BUSINESS = 'BUSINESS', 'Business Risk'

    class Status(models.TextChoices):
        OPEN = 'OPEN', 'Open'
        MITIGATING = 'MITIGATING', 'Mitigating'
        CLOSED = 'CLOSED', 'Closed'

    project = models.ForeignKey(
        'projects.Project',
        on_delete=models.CASCADE,
        related_name='risks'
    )

    title = models.CharField(max_length=200)

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=Category.choices
    )

    probability = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        help_text='Enter a value between 0.00 and 1.00'
    )

    impact = models.PositiveSmallIntegerField(
        help_text='Enter an impact value between 1 and 5'
    )

    mitigation_plan = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN
    )

    identified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='identified_risks'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def risk_exposure(self):
        return round(float(self.probability) * self.impact, 2)

    def __str__(self):
        return f"{self.title} - {self.project.name}"
