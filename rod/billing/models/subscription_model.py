import uuid

from django.db import models

from rod.accounts.models.customer_model import Customer
from rod.common.models import BaseModel
from rod.core.exceptions import ApplicationError
from rod.plan.models.plan_model import Plan


# Create your models here.
class Subscription(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    billing_cycle_day = models.CharField(max_length=255)
    billing_frequency = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.customer.name} - {self.plan.name}"

    def clean(self):
        if (
            self.start_date is not None
            and self.end_date is not None
            and self.start_date > self.end_date
        ):
            msg = "Start date must be before end date"
            raise ApplicationError(msg)

    class Meta:
        ordering = ["start_date"]
