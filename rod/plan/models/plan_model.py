from django.db import models

from rod.common.models import BaseModel


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    max_rows_processed = models.BigIntegerField()
    cost_per_million_rows = models.DecimalField(max_digits=10, decimal_places=2)
    base_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class PlanFeature(BaseModel):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name="features")
    feature_name = models.CharField(max_length=255)
    feature_description = models.TextField()

    def __str__(self):
        return f"{self.plan.name} - {self.feature_name}"

    class Meta:
        ordering = ["plan__name", "feature_name"]
