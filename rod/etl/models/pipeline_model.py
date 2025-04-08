import uuid

from django.db import models

from rod.billing.models.subscription_model import Subscription
from rod.common.models import BaseModel
from rod.etl.models.connector_model import ConnectorInstance


class Pipeline(BaseModel):
    class StatusChoices(models.TextChoices):
        PENDING = "PENDING", "Pending"
        DEPLOYING = "DEPLOYING", "Deploying"
        ACTIVE = "ACTIVE", "Active"
        FAILED = "FAILED", "Failed"
        STOPPED = "STOPPED", "Stopped"
        DELETED = "DELETED", "Deleted"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    connector_instance = models.ForeignKey(
        ConnectorInstance,
        on_delete=models.CASCADE,
        related_name="pipelines",
    )
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING,
    )
    notes = models.TextField()

    def __str__(self):
        return f"{self.id}"


class PipelineInstance(BaseModel):
    class StatusChoices(models.TextChoices):
        STARTED = "STARTED", "Started"
        RUNNING = "RUNNING", "Running"
        SUCCESS = "SUCCESS", "Success"
        FAILED = "FAILED", "Failed"
        CANCELLED = "CANCELLED", "Cancelled"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pipeline = models.ForeignKey(Pipeline, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.STARTED,
    )
    error = models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.id}"
