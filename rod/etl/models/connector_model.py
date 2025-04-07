import json
import uuid

from django.db import models

from rod.billing.models.subscription_model import Subscription
from rod.common.models import BaseModel
from rod.etl.utils.kms_helper import KMSHelper


class Connector(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    code = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ConnectorInstance(BaseModel):
    ACTIVATE = "A"
    INACTIVE = "I"
    FAILED = "F"
    PENDING = "P"

    STATUS_CHOICES = [
        (ACTIVATE, "Active"),
        (INACTIVE, "Inactive"),
        (FAILED, "Failed"),
        (PENDING, "Pending"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE)
    encrypted_config = models.JSONField()
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=INACTIVE)

    def __str__(self):
        return f"{self.subscription.customer.name} - {self.connector.name}"

    @property
    def decrypted_config(self) -> dict:
        if not self.encrypted_config:
            return {}
        plaintext = KMSHelper().decrypt(self.encrypted_config)
        return json.loads(plaintext)
