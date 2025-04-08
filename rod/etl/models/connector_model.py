import json
import uuid

from django.db import models

from rod.billing.models.subscription_model import Subscription
from rod.common.models import BaseModel
from rod.etl.utils.utils import KMSUtil


class Connector(BaseModel):
    class InputType(models.TextChoices):
        CONFIG_FORM = "config_form", "Config Form"
        FILE_UPLOAD = "file_upload", "File Upload"

    code = models.CharField(max_length=255, unique=True, primary_key=True)
    label = models.CharField(max_length=255)
    input_type = models.CharField(
        max_length=50,
        choices=InputType.choices,
        default=InputType.CONFIG_FORM,
    )
    config_form = models.JSONField(blank=True, null=True)

    def __str__(self):
        return self.label


class ConnectorInstance(BaseModel):
    class SchemaStatusChoices(models.TextChoices):
        NONE = "None", "None"
        DISCOVERING = "DISCOVERING", "Discovering"
        READY = "READY", "Ready"
        FAILED = "FAILED", "Failed"

    class StatusChoices(models.TextChoices):
        NONE = "None", "None"
        VALID = "VALID", "Valid"
        INVALID = "INVALID", "Invalid"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.SET_NULL,
        null=True,
        related_name="connector_instances",
    )
    connector = models.ForeignKey(
        Connector,
        on_delete=models.SET_NULL,
        null=True,
        related_name="instances",
    )
    encrypted_config = models.JSONField()
    schema_snapshot = models.JSONField(blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.NONE,
    )
    schema_status = models.CharField(
        max_length=20,
        choices=SchemaStatusChoices.choices,
        default=SchemaStatusChoices.NONE,
    )

    def __str__(self):
        return f"{self.id}"

    @property
    def customer_key_id(self) -> str:
        try:
            return self.subscription.customer_key_id
        except Exception:  # noqa: BLE001
            return None

    @property
    def decrypted_config(self) -> dict:
        if not self.encrypted_config:
            return {}
        plaintext = KMSUtil().decrypt(self.customer_key_id, self.encrypted_config)
        return json.loads(plaintext)
