from django.db import models

from rod.common.models import BaseModel
from rod.etl.models.connector_model import ConnectorInstance


class SourceSchemaSnapshot(BaseModel):
    connector_instance = models.ForeignKey(ConnectorInstance, on_delete=models.CASCADE)
    table_name = models.CharField(max_length=255)
    columns = models.JSONField()
    detected_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (
            f"{self.connector_instance.subscription.customer.name} - {self.table_name}"
        )
