from django.db import models

from rod.billing.models.subscription_model import Subscription
from rod.common.models import BaseModel
from rod.etl.models.connector_model import ConnectorInstance


class DeployedPipeline(BaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    source_connector = models.ForeignKey(
        ConnectorInstance,
        on_delete=models.CASCADE,
        related_name="source_connector",
    )
    destination_connector = models.ForeignKey(
        ConnectorInstance,
        on_delete=models.CASCADE,
        related_name="destination_connector",
    )
    sync_frequency = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    deployed_at = models.DateTimeField()
    notes = models.TextField()

    def __str__(self):
        return (
            f"{self.subscription.customer.name} - "
            f"{self.source_connector.connector.name} to "
            f"{self.destination_connector.connector.name}"
        )


class PipelineDatasetMapping(BaseModel):
    SYNC_MODE_FULL = "full"
    SYNC_MODE_INCREMENTAL = "incremental"
    SYNC_MODE_CHOICES = [
        (SYNC_MODE_FULL, "Full"),
        (SYNC_MODE_INCREMENTAL, "Incremental"),
    ]
    deployed_pipeline = models.ForeignKey(DeployedPipeline, on_delete=models.CASCADE)
    source_table_name = models.CharField(max_length=255)
    destination_table_name = models.CharField(max_length=255)
    column_mapping = models.JSONField()
    sync_mode = models.CharField(max_length=255, choices=SYNC_MODE_CHOICES)
    cursor_field = models.CharField(max_length=255)
    last_synced_at = models.DateTimeField()


class PipelineRunLog(BaseModel):
    deployed_pipeline = models.ForeignKey(DeployedPipeline, on_delete=models.CASCADE)
    run_id = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    rows_synced = models.BigIntegerField()
    status = models.CharField(max_length=255)
    error = models.TextField()
    log_data = models.JSONField()

    def __str__(self):
        return f"{self.deployed_pipeline.subscription.customer.name} - {self.run_id}"
