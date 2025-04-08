from django.db import models

from rod.common.models import BaseModel


class Plan(BaseModel):
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255, unique=True, primary_key=True)
    description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]


class PlanFeature(BaseModel):
    plan = models.ForeignKey(
        Plan,
        on_delete=models.SET_NULL,
        related_name="features",
        null=True,
    )
    code = models.CharField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"{self.plan.name} - {self.name}"

    class Meta:
        ordering = ["plan__name", "name"]
