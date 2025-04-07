from django.db import models

from rod.billing.models.subscription_model import Subscription
from rod.common.models import BaseModel
from rod.etl.models.connector_model import Connector


class SubscriptionConnector(BaseModel):
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    connector = models.ForeignKey(Connector, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.subscription.customer.name} - {self.connector.name}"
